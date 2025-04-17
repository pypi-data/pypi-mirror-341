from __future__ import annotations
import requests
import re
import json
import logging
import socket
from tenacity import retry, wait_exponential
from datetime import datetime
from cw_rpa import HttpClient

LOG = logging.getLogger("py_net_diags.cw_api")

class ConnectWiseAPIBase:
    """Base class for ConnectWise API interactions with core request functionality."""
    
    def __init__(self, cache=None, log=None, http_client: HttpClient = None):
        from .cache_manager import CacheManager
        from .config_manager import ConfigManager
        self.log = log if log is not None else LOG
        self.config = ConfigManager(log=self.log).config
        self.running_in_asio = self.config.get('running_in_asio')
        
        self.log.debug(f"Initializing ConnectWise API running in Asio: {self.running_in_asio}")
        
        
        self.auth = f"Basic {self.config.get('auth')}"
        self.client_id = self.config.get('client_id')
        self.base_url = self.config.get('base_url')
        self.max_retries = self.config.get('retry_attempts', 5)
        self.retry_delay = self.config.get('retry_delay', 15)
        
        
        self.cache = cache if cache is not None else CacheManager(running_in_asio=self.running_in_asio, log=self.log)
        
        self.log.debug(f"ConnectWise API Base initialized with base URL: {self.base_url} Retry attempts: {self.max_retries} Retry delay: {self.retry_delay}ms Running in Asio: {self.running_in_asio}")
        
        if self.running_in_asio:
            try:
                self.http_client = http_client if http_client is not None else HttpClient()
                self.client = self.http_client.third_party_integration("cw_psa")
            except Exception as e:
                self.log.exception(f"Failed to initialize HTTP client: {str(e)}", stack_info=True)
                self.log.debug(f"Http Client: {self.http_client}")
        else:
            self.headers = self._setup_headers()
    
    def _setup_headers(self):
        """Setup and log API headers with sensitive data masked"""
        headers = {
            "Authorization": self.auth,
            "ClientID": self.client_id,
            "Content-Type": "application/json"
        }
        
        # Mask sensitive data for logging
        filtered_auth = re.sub(r'(?<=.{8}).', '*', headers['Authorization'])
        filtered_clientId = re.sub(r'(?<=.{8}).', '*', headers['ClientID'])
        filtered_headers = {
            "Authorization": filtered_auth,
            "ClientID": filtered_clientId,
            "Content-Type": headers['Content-Type']
        }
        self.log.debug(f"Headers: {json.dumps(filtered_headers, indent=2)}")
        
        return headers
        
    def _is_retryable_response(self, response):
        """Instance method version for response validation"""
        if response.status_code >= 500 or response.status_code == 429:
            self.log.debug(f"Retryable response: {response.status_code}")
            return True
        return False
    
    @retry(
        stop=lambda rs: rs.attempt_number >= rs.args[0].max_retries + 1,
        wait=lambda rs: wait_exponential(multiplier=rs.args[0].retry_delay)(rs),
        retry=lambda rs: rs.args[0]._is_retryable_response(rs.outcome.result()) if rs.outcome else True,
        reraise=True
    )
    def make_request(self, method: str, url: str, paginate: bool = True, page_size: int = 1000, **kwargs) -> requests.Response:
        """make_request: _summary_

        Description: _description_

        Args:
            method (str): _description_
            url (str): _description_
            paginate (bool, optional): _description_. Defaults to True.
            page_size (int, optional): _description_. Defaults to 1000.

        Returns:
            requests.Response: _description_
        """
        try:
            # Initial request parameters
            if self.running_in_asio:
                # Check if we have file uploads in the request
                if 'files' in kwargs:
                    # If Content-Type is already set in headers, remove it as it will be set automatically for multipart uploads
                    if 'headers' in kwargs and 'Content-Type' in kwargs['headers']:
                        del kwargs['headers']['Content-Type']
                
                request_func = lambda u, **kw: getattr(self.client, method)(url=u, **kw)
            else:
                kwargs_with_headers = kwargs.copy()
                # For non-ASIO, ensure headers are set properly but don't override Content-Type if files are being uploaded
                if 'files' in kwargs and 'headers' in kwargs_with_headers and 'Content-Type' in kwargs_with_headers['headers']:
                    headers_copy = kwargs_with_headers['headers'].copy()
                    del headers_copy['Content-Type']
                    kwargs_with_headers['headers'] = {**self.headers, **headers_copy}
                else:
                    kwargs_with_headers['headers'] = self.headers
                
                request_func = lambda u, **kw: getattr(requests, method)(url=u, **{**kwargs_with_headers, **kw})
            
            # For non-GET requests or if pagination is disabled, just make a normal request
            if method.lower() != "get" or not paginate:
                response = request_func(url, **kwargs)
                response.raise_for_status()
                return response
                
            # Handle pagination for GET requests
            all_results = []
            original_url = url
            page = 1
            has_more_pages = True
            original_response = None
            
            # Pagination loop
            while has_more_pages:
                # Prepare URL with pagination parameters
                current_url = original_url
                
                # Add pagination parameters if not already present
                if "page=" not in current_url:
                    separator = "&" if "?" in current_url else "?"
                    current_url = f"{current_url}{separator}page={page}"
                else:
                    # Update existing page parameter
                    current_url = re.sub(r"page=\d+", f"page={page}", current_url)
                    
                # Add page size if not already present
                if "pageSize=" not in current_url:
                    current_url = f"{current_url}&pageSize={page_size}"
                    
                # Make the request for this page
                response = request_func(current_url, **kwargs)
                response.raise_for_status()
                
                # Keep the first response for headers and status
                if page == 1:
                    original_response = response
                    
                # Parse the response based on content type
                page_data = response.json()
                
                # Different APIs handle pagination differently
                if isinstance(page_data, list):
                    # API returns a simple array
                    all_results.extend(page_data)
                    # If we got fewer results than page_size, we're done
                    if len(page_data) < page_size:
                        has_more_pages = False
                        self.log.debug(f"Retrieved {len(page_data)} results (less than page size). This is the last page.")
                elif isinstance(page_data, dict):
                    # API returns a dictionary with items and pagination metadata
                    if 'items' in page_data:
                        # Standard format with items array
                        all_results.extend(page_data['items'])
                        # Check pagination metadata
                        if (page_data.get('totalPages', 0) <= page or 
                            page_data.get('hasMorePages', True) is False or
                            page_data.get('nextPage') is None):
                            has_more_pages = False
                            self.log.debug("Reached last page based on pagination metadata")
                    else:
                        # Non-standard format, just add the whole object and stop
                        all_results.append(page_data)
                        has_more_pages = False
                else:
                    # Unusual response format, add as is and stop
                    all_results.append(page_data)
                    has_more_pages = False
                    
                # Move to next page if needed
                if has_more_pages:
                    page += 1
                    
            # Create a modified response with combined results
            if original_response:
                # Preserve the original response properties but replace the content
                original_response._content = json.dumps(all_results).encode('utf-8')
                original_response.headers['X-Total-Pages'] = str(page)
                original_response.headers['X-Total-Items'] = str(len(all_results))
                return original_response
            else:
                return response
                
        except requests.exceptions.RequestException as e:
            self.log.exception(f"Request failed with error: {str(e)}", stack_info=True)
            raise


class ConnectWiseServiceAPI(ConnectWiseAPIBase):
    """Specialized API class for service-related operations in ConnectWise."""
    
    def __init__(self, cache = None, log = None):
        super().__init__(cache)
        self.log = log if log is not None else LOG
        
    def get_ticket_attachments(self, ticket_id: int) -> list:
        """
        Get all attachments for a ticket
        
        Args:
            ticket_id: The ConnectWise ticket ID
            
        Returns:
            list: Attachment metadata objects
        """
        cache_key = f"ticket_attachments_{ticket_id}"
        cached_statuses = self.cache.get("ticket_attachments", cache_key)
        if cached_statuses is not None:
            self.log.debug(f"Retrieved cached attachments for ticket {ticket_id}")
            return cached_statuses
        
        url = f"{self.base_url}/system/documents?recordType=Ticket&recordId={ticket_id}"
        self.log.debug(f"Fetching attachments for ticket ID: {ticket_id}")
        
        response = self.make_request("get", url)
        
        if response.status_code == 200:
            attachments = response.json()
            self.cache.set("ticket_attachments", cache_key, attachments)
            self.log.debug(f"Retrieved {len(attachments)} attachments for ticket {ticket_id}")
            return attachments
        else:
            self.log.error(f"Failed to fetch attachments for ticket {ticket_id}: {response.status_code}")
            self.log.error(f"Failed to cache attachments for ticket {ticket_id} -> {response.text}")
            self.log.debug(f"Response content: {response.text}")
            return []
        
    def upload_attachment(self, ticket_id: int, file_path: str, title: str = None, filename: str = None) -> None:
        if not title:
            hostname = socket.gethostname()
            timestamp = datetime.now().strftime("%m-%d %H:%M")
            title = f'network diagnostics {hostname} {timestamp}'
    
        if not filename:
            filename = title.replace(" ", "_") + ".pdf"
        
        url = f"{self.base_url}/system/documents"
        
        # Ensure file is opened in binary mode
        with open(file_path, 'rb') as file_obj:
            # Prepare the files data properly for multipart form upload
            files = {
                'file': (filename, file_obj, 'application/pdf')
            }
        
            data = {
                'recordId': str(ticket_id),
                'recordType': 'Ticket',
                'title': title.title(),
            }
        
            # Make sure Content-Type header is NOT set, letting the request library set it automatically
            headers = self.headers.copy() if hasattr(self, 'headers') else {}
            if 'Content-Type' in headers:
                del headers['Content-Type']
        
            # Make the POST request with files and data parameters
            try:
                self.log.debug(f"Uploading attachment {filename} to ticket {ticket_id}")
                response = self.make_request("post", url, paginate=False, files=files, data=data, headers=headers)
        
                # Check the response
                self.log.debug(f"Upload response status: {response.status_code}")
                self.log.debug(f"Upload response content: {response.text}")
                return response.json() if response.status_code == 200 else None
            except Exception as e:
                self.log.error(f"Error uploading attachment: {str(e)}")
                return None
            
    def add_ticket_note(self, ticket_id: int, note_text: str, internal: bool = True) -> dict:
        """
        Add a note to a ticket
        
        Args:
            ticket_id: The ConnectWise ticket ID
            note_text: Text content of the note
            internal: Whether the note is internal-only (True) or customer-visible (False)
            
        Returns:
            dict: Created note information or None if failed
        """
        url = f"{self.base_url}/service/tickets/{ticket_id}/notes"
        
        payload = {
            "text": note_text,
            "internalAnalysisFlag": internal,
            "detailDescriptionFlag": False,
            "resolutionFlag": False
        }
        
        self.log.debug(f"Adding {'internal' if internal else 'customer-visible'} note to ticket {ticket_id}")
        
        response = self.make_request("post", url, json=payload)
        
        if response.status_code in [200, 201]:
            note_data = response.json()
            self.log.debug(f"Successfully added note to ticket {ticket_id}")
            self.log.debug(f"Note ID: {note_data.get('id')}")
            return note_data
        else:
            self.log.error(f"Failed to add note to ticket {ticket_id}: {response.status_code}")
            self.log.debug(f"Response content: {response.text}")
            return None
    