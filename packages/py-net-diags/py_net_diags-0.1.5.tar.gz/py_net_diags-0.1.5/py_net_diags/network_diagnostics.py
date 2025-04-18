import logging

LOG = logging.getLogger("py_net_diags.network_diagnostics")

try:
    import traceback
    import subprocess
    import platform
    import socket
    import psutil
    import json
    import requests
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    import markdown
    from xhtml2pdf import pisa
    from datetime import datetime
    import speedtest
    import re
    import importlib.util
except Exception as e:
    LOG.info(f"Error importing required modules: {traceback.format_exc()}")

class NetworkDiagnostics:
    """Class for performing network diagnostics and generating reports."""
    
    def __init__(self, log=None):
        """
        Initialize the NetworkDiagnostics class.
        
        Args:
            logger: Logger object to use for logging. If None, uses the default logger.
        """
        self.socket = socket
        self.psutil = psutil
        self.platform = platform
        self.subprocess = subprocess
        self.json = json
        self.traceback = traceback
        self.datetime = datetime
        self.markdown = markdown
        self.importlib = importlib.util
        
        # Store retry decorators
        self.retry = retry
        self.retry_if_exception_type = retry_if_exception_type
        self.wait_exponential = wait_exponential
        self.stop_after_attempt = stop_after_attempt
        
        # Store exceptions
        self.ConnectionError = ConnectionError
        self.TimeoutError = TimeoutError
        self.requests_exceptions = requests.exceptions
        
        # Setup logger
        self.logger = log if log is not None else LOG
    
    def get_hostname_and_ip(self):
        """Get the hostname and IP address of the machine."""
        result = {
            "hostname": self.socket.gethostname()
        }
        
        try:
            result["ip_address"] = self.socket.gethostbyname(self.socket.gethostname())
        except self.socket.gaierror:
            # Fallback method to get IP address
            try:
                s = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                result["ip_address"] = s.getsockname()[0]
                s.close()
            except Exception:
                result["ip_address"] = f"Error retrieving IP: {self.traceback.format_exc()}"
                self.logger.exception(f"An exception occurred while executing function get_hostname_and_ip: {self.traceback.format_exc()}", stack_info=True)
        
        return result
    
    def get_last_reboot_time(self):
        """Get the last reboot time of the machine."""
        try:
            boot_time = self.psutil.boot_time()
            timestamp = self.human_readable_timestamp(boot_time)
            return {"last_reboot": timestamp}
        except Exception:
            self.logger.exception(f"An exception occurred while executing function get_last_reboot_time: {self.traceback.format_exc()}", stack_info=True)
            return {"last_reboot": f"Error retrieving boot time: {self.traceback.format_exc()}"}
    
    def run_ping_tests(self, targets=None):
        """
        Run ping tests to specified targets with status indicators based on response time.
        
        Args:
            targets: Additional targets to ping. Can be string, list, tuple, set, or dict keys.
                    If None, uses default targets.
        
        Returns:
            dict: Dictionary with ping test results including response time and status
        """
        
        # Default targets
        default_targets = ["8.8.8.8", "1.1.1.1", "google.com", "amazon.com"]
        
        # Process input targets and combine with defaults
        all_targets = []
        
        # Add user-provided targets
        if targets is not None:
            if isinstance(targets, str):
                all_targets.append(targets)
            elif isinstance(targets, (list, tuple)):
                all_targets.extend(targets)
            elif isinstance(targets, set):
                all_targets.extend(list(targets))
            elif isinstance(targets, dict):
                all_targets.extend(list(targets.keys()))
            else:
                return {"ping_tests": {"error": f"Invalid targets type: {type(targets).__name__}"}}
        
        # Add default targets
        all_targets.extend(default_targets)
        
        # Remove duplicates while preserving order (first occurrence stays)
        seen = set()
        unique_targets = [x for x in all_targets if not (x in seen or seen.add(x))]
        
        # Define time thresholds for status (in ms)
        thresholds = {
            "excellent": 20,    # 0-20ms: Excellent
            "good": 50,         # 21-50ms: Good
            "fair": 100,        # 51-100ms: Fair
            "poor": 200         # 101-200ms: Poor
                                # >200ms: Critical
        }
        
        # Run ping tests
        results = {}
        
        for target in unique_targets:
            if not isinstance(target, str):
                results[str(target)] = {"response": f"Invalid target type: {type(target).__name__}", "status": "error"}
                continue
                
            try:
                if self.platform.system() == "Windows":
                    ping_output = self.subprocess.check_output(["ping", "-n", "3", target], text=True)
                    # Windows ping output parsing
                    if "Average" in ping_output:
                        avg_line = [line for line in ping_output.split('\n') if "Average" in line][0]
                        avg_ms = float(avg_line.split('=')[-1].strip().split()[0].replace('ms', '').strip())
                        time_str = f"{avg_ms} ms"
                    else:
                        results[target] = {"response": "Ping successful, but couldn't extract average time", "status": "unknown"}
                        continue
                else:
                    # Linux/macOS ping output parsing
                    ping_output = self.subprocess.check_output(["ping", "-c", "3", target], text=True)
                    if "avg" in ping_output:
                        avg_line = [line for line in ping_output.split('\n') if "avg" in line][0]
                        # Format typically: rtt min/avg/max/mdev = 15.471/17.738/20.754/2.233 ms
                        avg_ms = float(avg_line.split('=')[1].strip().split('/')[1])
                        time_str = f"{avg_ms} ms"
                    else:
                        results[target] = {"response": "Ping successful, but couldn't extract average time", "status": "unknown"}
                        continue
                
                # Determine status based on response time
                if avg_ms <= thresholds["excellent"]:
                    status = "excellent"
                elif avg_ms <= thresholds["good"]:
                    status = "good"
                elif avg_ms <= thresholds["fair"]:
                    status = "fair"
                elif avg_ms <= thresholds["poor"]:
                    status = "poor"
                else:
                    status = "critical"
                    
                results[target] = {"response": time_str, "status": status, "time_ms": avg_ms}
                
            except Exception as e:
                results[target] = {"response": f"Failed: {str(e)}", "status": "error"}
                self.logger.exception(f"An exception occurred while executing function run_ping_tests: {self.traceback.format_exc()}", stack_info=True)
        
        return {"ping_tests": results}
    
    def _create_speedtest_retry_decorator(self):
        """Create and return the retry decorator for speed tests."""
        return self.retry(
            retry=self.retry_if_exception_type((
                self.ConnectionError, 
                self.TimeoutError,
                self.requests_exceptions.HTTPError,
                self.requests_exceptions.ConnectionError,
                self.requests_exceptions.Timeout
            )),
            wait=self.wait_exponential(multiplier=1, min=2, max=30),
            stop=self.stop_after_attempt(5),
            reraise=True,
            before_sleep=lambda retry_state: self.logger.info(f"Speedtest attempt {retry_state.attempt_number} failed, retrying in {retry_state.next_action.sleep} seconds...")
        )
    
    def _run_speedtest_with_retry(self):
        """Inner function to run speedtest with retry logic"""
        
        retry_decorator = self._create_speedtest_retry_decorator()
        
        @retry_decorator
        def run_test():
            st = speedtest.Speedtest()
            st.get_best_server()
            
            # Run download test
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            
            # Run upload test
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            
            # Get ping
            ping = st.results.ping
            
            return {
                "download speed": f"{download_speed:.2f} Mbps",
                "upload speed": f"{upload_speed:.2f} Mbps",
                "ping latency": f"{ping:.2f} ms"
            }
            
        return run_test()
    
    def run_speed_test(self):
        """Run an internet speed test with multiple providers and fallback options."""
        results = {}
        
        # Try multiple speed test providers in order of preference
        providers = [
            {"name": "Speedcheck", "function": self.run_speedcheck_cli},
            {"name": "Speedtest", "function": self.run_speedtest_cli_test},
        ]
        
        for provider in providers:
            try:
                self.logger.info(f"Attempting speed test using {provider['name']}...")
                provider_results = provider["function"]()
                
                if provider_results and "error" not in provider_results:
                    results = provider_results
                    if provider["name"] != "Speedcheck":
                        results["provider"] = provider["name"]
                    self.logger.info(f"Speed test completed successfully using {provider['name']}")
                    break
                else:
                    self.logger.warning(f"Speed test with {provider['name']} failed, trying next provider...")
                    self.logger.warning(f"Speed test results: {provider_results}")
            except Exception as e:
                self.logger.warning(f"Error running {provider['name']} speed test: {str(e)}")
        
        # If all providers failed, report a simple error
        if not results or "error" in results:
            results = {
                "download": "Failed to retrieve",
                "upload": "Failed to retrieve",
                "ping": "Failed to retrieve",
                "provider": "None",
                "error": "All speed test providers failed"
            }
            self.logger.error("All speed test providers failed")
        
        return {"speed_test": results}
    
    def _run_speedcheck(self, test: str):
        try:
            base_cmd = ["speedcheck", "run", "--type"]

            cmd = base_cmd + [test["cmd"]]
            self.logger.info(f"Running {test['name']} speed test... -> {cmd}")
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode != 0:
                return {"error": process.stderr}
            
            # Find the JSON output in the result - use more lenient pattern
            output = process.stdout
            match = re.search(r'({.*})', output, re.DOTALL)
            
            if match:
                json_str = match.group(1)
                try:
                    # Parse the JSON string
                    result = json.loads(json_str)
                    return {"result": result}
                except json.JSONDecodeError as e:
                    return {"error": f"Failed to parse JSON: {str(e)}"}
            else:
                return {"error": "Could not find JSON in output"}
        except Exception as e:
            return {"error": f"An error occurred while running speedcheck: {str(e)}"}
            
    def _parse_speedcheck_results(self, results: dict) -> dict:
        """
        parse_results: Parses the results from the speed test.

        Usage:
        
        1. parse_results(results)

        Args:
            results (dict): The results from the speed test as a dictionary.

        Returns:
            dict: A dictionary containing the parsed speed test results.
        """
        download_keys = [
            "Download speed", "download_speed",
        ]
        upload_keys = [
            "Upload speed", "upload_speed"
        ]
        ping_keys = [
            "Ping", "ping_speed", "Latency", "ping_time", "ping_ms", "ping_rtt"
        ]
        jitter_keys = [
            "Jitter", "jitter"
        ]
        isp_name_keys = [
            "ISP Name", "isp_name"
        ]
        
        download_speed = None  # Will display "Not available" if None later
        upload_speed = None
        ping = None
        jitter = None
        isp_name = None
        
        download_keys_lower = [key.lower() for key in download_keys]
        upload_keys_lower = [key.lower() for key in upload_keys]
        ping_keys_lower = [key.lower() for key in ping_keys]
        jitter_keys_lower = [key.lower() for key in jitter_keys]
        isp_name_keys_lower = [key.lower() for key in isp_name_keys]
        
        for key, value in results.items():
            key_lower = key.lower()  # Convert each dictionary key to lowercase
            
            if key_lower in download_keys_lower:
                download_speed = value
            elif key_lower in upload_keys_lower:
                upload_speed = value
            elif key_lower in ping_keys_lower:
                ping = value
            elif key_lower in jitter_keys_lower:
                jitter = value
            elif key_lower in isp_name_keys_lower:
                isp_name = value
        
        result = {}
        if download_speed is not None:
            result["download speed"] = f"{download_speed}"
        if upload_speed is not None:
            result["upload speed"] = f"{upload_speed}"
        if ping is not None:
            result["ping latency"] = f"{ping}"
        if jitter is not None:
            result["jitter"] = f"{jitter}"
        if isp_name is not None:
            result["isp name"] = f"{isp_name}"

        return result
    
    def run_speedcheck_cli(self):
        all_tests = [
            { "name": "SpeedSmart", "cmd": "speedsmart" },
            { "name": "Open Speed Test", "cmd": "openspeedtest" },
            { "name": "Ookla", "cmd": "ookla" },
            { "name": "Fast", "cmd": "fast" }
        ]
        
        results = {}  # Initialize results dictionary
        
        if self.importlib.find_spec("speedcheck") is None:
            try:
                self.subprocess.run(["pip", "install", "speedcheck"], check=True)
                self.logger.info("Speedcheck installed successfully")
            except self.subprocess.CalledProcessError as e:
                return {"error": f"Failed to install speedcheck: {e}"}
        
        for test in all_tests:
            test_result = self._run_speedcheck(test)
            
            if "result" in test_result and test_result["result"]:
                parsed_results = self._parse_speedcheck_results(test_result["result"])
                self.logger.info(f"Parsed speed test results for {test['name']}: {parsed_results}")
                if parsed_results.get("download speed"):
                    results = parsed_results
                    results["provider"] = test["name"]  # Add provider info
                    self.logger.info(f"Speed test completed successfully using {test['name']}")
                    return results
        
        # If all tests failed, return error
        return {"error": "All speedcheck tests failed"}

    def run_speedtest_cli_test(self):
        """Original speedtest-cli function (kept as last fallback)."""
        results = {}
        try:
            try:
                results = self._run_speedtest_with_retry()
            except ImportError:
                results["error"] = "Speedtest module not found"
            except Exception as e:
                results["error"] = f"Speed test failed: {str(e)}"
        except Exception as e:
            results["error"] = f"Speed test failed: {str(e)}"
        
        return results
    
    def get_network_interfaces_info(self):
        """Get information about network interfaces."""
        results = {}
        try:
            net_io = self.psutil.net_io_counters(pernic=True)
            net_addrs = self.psutil.net_if_addrs()
            
            for interface, stats in net_io.items():
                if interface in net_addrs:
                    results[interface] = {
                        "bytes_sent": f"{stats.bytes_sent / (1024 * 1024):.2f} MB",
                        "bytes_recv": f"{stats.bytes_recv / (1024 * 1024):.2f} MB",
                        "addresses": []
                    }
                    
                    for addr in net_addrs[interface]:
                        if addr.family == self.socket.AF_INET:  # IPv4
                            results[interface]["addresses"].append({
                                "type": "IPv4",
                                "address": addr.address,
                                "netmask": addr.netmask
                            })
                        elif addr.family == self.socket.AF_INET6:  # IPv6
                            results[interface]["addresses"].append({
                                "type": "IPv6",
                                "address": addr.address
                            })
        except Exception:
            results["error"] = f"Failed to get network interface info: {self.traceback.format_exc()}"
            self.logger.exception(f"Error retrieving network interface info: {self.traceback.format_exc()}", stack_info=True)
        
        return {"network_interfaces": results}
    
    def build_diagnostics_dict(self, additional_targets=None):
        """Build a comprehensive diagnostics dictionary using all the individual functions."""
        diagnostics = {}
        
        # Add hostname and IP address
        diagnostics.update(self.get_hostname_and_ip())
        
        # Add last reboot time
        diagnostics.update(self.get_last_reboot_time())
        
        # Add ping tests
        diagnostics.update(self.run_ping_tests(targets=additional_targets))
        
        # Add speed test
        diagnostics.update(self.run_speed_test())
        
        # Add network interfaces information
        diagnostics.update(self.get_network_interfaces_info())
        
        # Add timestamp for when the diagnostics were collected
        diagnostics["timestamp"] = self.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        diagnostics["human_timestamp"] = self.human_readable_timestamp(diagnostics["timestamp"])
        
        return diagnostics
    
    def format_diagnostics(self, diagnostics):
        """
        Format the diagnostics dictionary as a readable string
        
        Args:
            diagnostics (dict): Dictionary containing diagnostic information
        
        Returns:
            str: Formatted diagnostics text
        """
        output = []
        
        output.append("="*50)
        output.append("NETWORK DIAGNOSTICS REPORT")
        output.append("="*50)
        
        output.append(f"\nHostname: {diagnostics['hostname']}")
        output.append(f"IP Address: {diagnostics['ip_address']}")
        output.append(f"Last Reboot: {diagnostics['last_reboot']}")
        
        output.append("\nPING TESTS:")
        for target, result in diagnostics['ping_tests'].items():
            output.append(f"  {target}: {self.format_ping_result(result)}")
        
        output.append("\nSPEED TEST:")
        for key, value in diagnostics['speed_test'].items():
            output.append(f"  {key.capitalize()}: {value}")
        
        output.append("\nNETWORK INTERFACES:")
        for interface, data in diagnostics['network_interfaces'].items():
            if isinstance(data, dict) and "error" not in data:
                output.append(f"  {interface}:")
                output.append(f"    Bytes Sent: {data['bytes_sent']}")
                output.append(f"    Bytes Received: {data['bytes_recv']}")
                
                if data['addresses']:
                    output.append("    IP Addresses:")
                    for addr in data['addresses']:
                        if addr['type'] == "IPv4":
                            output.append(f"      {addr['type']}: {addr['address']} (Netmask: {addr['netmask']})")
                        else:
                            output.append(f"      {addr['type']}: {addr['address']}")
            else:
                output.append(f"  {interface}: {data}")
        
        return "\n".join(output)
    
    def format_diagnostics_as_markdown(self, diagnostics):
        """
        Format the diagnostics dictionary as professional Markdown for PDF conversion
        
        Args:
            diagnostics (dict): Dictionary containing diagnostic information
        
        Returns:
            str: Formatted diagnostics as Markdown
        """
        output = []
        
        # Summary section
        output.append("## Summary")
        output.append("This report contains network diagnostics information including:")
        output.append("- Basic system information")
        output.append("- Ping test results to major DNS providers and websites")
        output.append("- Internet speed test results showing upload and download speeds")
        output.append("- Detailed information about network interfaces")
        output.append("")
        
        # System Information Section
        output.append("## System Information")
        
        output.append("| Parameter | Value |")
        output.append("|:----------|:------|")
        output.append(f"| Hostname | {diagnostics['hostname']} |")
        output.append(f"| IP Address | {diagnostics['ip_address']} |")
        output.append(f"| Last Reboot | {diagnostics['last_reboot']} |")
        output.append("")
        
        # Ping Tests Section
        output.append("## Ping Tests")
        
        output.append("| Target | Response Time |")
        output.append("|:-------|:--------------|")
        for target, result in diagnostics['ping_tests'].items():
            output.append(f"| {target} | {result} |")
        output.append("")
        
        # Speed Test Section
        output.append("## Internet Speed Test")
        
        output.append("| Metric | Value |")
        output.append("|:-------|:------|")
        for key, value in diagnostics['speed_test'].items():
            # Capitalize the key and replace underscores with spaces
            formatted_key = key.replace('_', ' ').capitalize()
            output.append(f"| {formatted_key} | {value} |")
        output.append("")
        
        # Network Interfaces Section
        output.append("## Network Interfaces")
        
        for interface, data in diagnostics['network_interfaces'].items():
            output.append(f"### {interface}")
            
            if isinstance(data, dict) and "error" not in data:
                output.append("| Metric | Value |")
                output.append("|:-------|:------|")
                output.append(f"| Bytes Sent | {data['bytes_sent']} |")
                output.append(f"| Bytes Received | {data['bytes_recv']} |")
                output.append("")
                
                if data['addresses']:
                    output.append("#### IP Addresses")
                    output.append("| Type | Address | Netmask |")
                    output.append("|:-----|:--------|:--------|")
                    for addr in data['addresses']:
                        if addr['type'] == "IPv4":
                            output.append(f"| {addr['type']} | {addr['address']} | {addr['netmask']} |")
                        else:
                            output.append(f"| {addr['type']} | {addr['address']} | - |")
                    output.append("")
            else:
                output.append(f"*Error: {data}*\n")
        
        return "\n".join(output)
    
    def print_diagnostics(self, diagnostics):
        """
        Print the network diagnostics in a readable format
        
        Args:
            diagnostics (dict): Dictionary containing diagnostic information
        """
        formatted_output = self.format_diagnostics(diagnostics)
        self.logger.info(formatted_output)
    
    def write_diagnostics_to_files(self, diagnostics, filename=None):
        """
        Write diagnostics data to a text file and also create a Markdown and PDF version.
        
        Args:
            diagnostics (dict): Dictionary containing diagnostic information
            filename (str, optional): Filename to write to. Defaults to network_diagnostics_{timestamp}.txt
        
        Returns:
            bool: True if successful, False otherwise
        """
        if filename is None:
            filename = "network_diagnostics.txt"
        
        try:
            with open(filename, 'w') as f:
                # First write a formatted readable version
                f.write(self.format_diagnostics(diagnostics))
                
                # Also write the raw JSON data for programmatic access
                f.write("\n\n")
                f.write("="*50 + "\n")
                f.write("RAW JSON DATA\n")
                f.write("="*50 + "\n")
                f.write(self.json.dumps(diagnostics, indent=2))
                
            self.logger.info(f"Diagnostics written to {filename}")
            try:
                markdown_diagnostics = self.format_diagnostics_as_markdown(diagnostics)
                full_md = markdown_diagnostics
                # Add title and timestamp
                md_output = []
                md_output.append("# Network Diagnostics Report")
                md_output.append(f"*Generated on: {diagnostics.get('timestamp', 'Not recorded')}*\n")
                md_output.append(full_md)
                final_ouput = "\n".join(md_output)
                with open(filename.replace('.txt', '.md'), 'w') as md_file:
                    md_file.write(final_ouput)
                output_path = filename.replace('.txt', '.pdf')
                self.logger.info(f"Markdown diagnostics written to {filename.replace('.txt', '.md')}")
                try:
                    self.markdown_to_pdf(markdown_diagnostics, output_filename=filename.replace('.txt', '.pdf'))
                    self.logger.info(f"PDF diagnostics written to {filename.replace('.txt', '.pdf')}")
                except Exception:
                    self.logger.exception(f"Error converting markdown to PDF: {self.traceback.format_exc()}", stack_info=True)
            except Exception:
                self.logger.exception(f"Error writing markdown diagnostics: {self.traceback.format_exc()}", stack_info=True)
            return True, output_path
        except Exception:
            self.logger.exception(f"Error writing diagnostics to file: {self.traceback.format_exc()}", stack_info=True)
            return False, None
    
    def markdown_to_pdf(self, markdown_content, output_filename=None, title=None, author=None):
        """
        Convert Markdown content to a nicely formatted PDF file using xhtml2pdf.
        
        Args:
            markdown_content (str): The Markdown content to convert
            output_filename (str, optional): The name of the output PDF file. 
                                            Defaults to "report.pdf".
            title (str, optional): The title of the PDF document.
                                  Defaults to "Network Diagnostics Report".
            author (str, optional): Author of the document.
                                   Defaults to "Network Diagnostics Tool".
        
        Returns:
            str: Path to the generated PDF file
        """
        
        # Set defaults
        if output_filename is None:
            output_filename = "network_diagnostics.pdf"
        
        if title is None:
            title = "Network Diagnostics Report"
            
        if author is None:
            author = "Network Diagnostics Tool"
        
        try:
            html = self.markdown.markdown(
                markdown_content,
                extensions=[
                    'markdown.extensions.tables',
                    'markdown.extensions.fenced_code',
                    'markdown.extensions.toc',
                    'markdown.extensions.nl2br'
                ]
            )
            
            # Add CSS styling for a professional look
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{title}</title>
                <style>
                    @page {{
                        size: letter;
                        margin: 1in;
                    }}
                    body {{
                        font-family: 'Helvetica', 'Arial', sans-serif;
                        font-size: 12px;
                        line-height: 1.6;
                        color: #333;
                    }}
                    h1 {{
                        font-size: 24px;
                        color: #2c3e50;
                        border-bottom: 1px solid #eee;
                        padding-bottom: 10px;
                        margin-top: 30px;
                    }}
                    h2 {{
                        font-size: 18px;
                        color: #2980b9;
                        margin-top: 25px;
                    }}
                    h3 {{
                        font-size: 16px;
                        color: #3498db;
                        margin-top: 20px;
                    }}
                    h4 {{
                        font-size: 14px;
                        color: #555;
                        margin-top: 15px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }}
                    th {{
                        background-color: #f5f5f5;
                        font-weight: bold;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f9f9f9;
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .footer {{
                        margin-top: 30px;
                        text-align: center;
                        font-size: 10px;
                        color: #777;
                    }}
                    code {{
                        font-family: monospace;
                        background-color: #f5f5f5;
                        padding: 2px 4px;
                        border-radius: 4px;
                    }}
                    pre {{
                        background-color: #f5f5f5;
                        padding: 10px;
                        border-radius: 4px;
                        overflow-x: auto;
                    }}
                    ul, ol {{
                        margin-left: 20px;
                    }}
                    li {{
                        margin-bottom: 5px;
                    }}
                    em, i {{
                        color: #555;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{title}</h1>
                    <p><em>Generated by {author}</em></p>
                    <p><em>Date: {self.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</em></p>
                </div>
                
                {html}
                
                <div class="footer">
                    <p>Generated on {self.datetime.now().strftime("%Y-%m-%d")} | Network Diagnostics Tool</p>
                    <pdf:pagenumber> of <pdf:pagecount>
                </div>
            </body>
            </html>
            """
            
            # Create a PDF file
            with open(output_filename, "wb") as result_file:
                # Convert HTML to PDF
                pisa_status = pisa.CreatePDF(
                    src=styled_html,
                    dest=result_file
                )
            
            # Return the output filename if successful
            if pisa_status.err:
                self.logger.error(f"Error generating PDF: {pisa_status.err}")
                return None
            else:
                self.logger.info(f"PDF report generated successfully: {output_filename}")
                return output_filename
                
        except ImportError:
            self.logger.exception("xhtml2pdf is not installed. Install with: pip install xhtml2pdf")
            return None
        except Exception:
            self.logger.exception(f"Error generating PDF: {self.traceback.format_exc()}", stack_info=True)
            return None
    
    def net_interface_string(self, net_interfaces: dict) -> list[str]:
        """Converts a dictionary of network interfaces to a list of formatted strings."""
        result = []
        
        for interface, interface_data in net_interfaces.items():
            # Access the dictionary fields correctly
            bytes_sent = interface_data['bytes_sent']
            bytes_recv = interface_data['bytes_recv']
            addresses = interface_data['addresses']
            
            if not addresses:
                ip_str = "None"
            else:
                ip_str = ", ".join([f"{addr['type']}: {addr['address']}" for addr in addresses])
            
            formatted_str = f"{interface}: sent: {bytes_sent}, recv: {bytes_recv}, IPs: {ip_str}"
            result.append(formatted_str)
        
        return result
    
    def human_readable_timestamp(self, timestamp):
        """Convert a timestamp to a human-readable format."""
        try:
            if isinstance(timestamp, str):
                # If timestamp is already a string, return it as is
                return timestamp
            elif isinstance(timestamp, (int, float)):
                # If timestamp is a number, assume it's a Unix timestamp
                return self.datetime.fromtimestamp(timestamp).strftime("%B %d, %Y %I:%M:%S %p")
            else:
                # If it's neither a string nor a number, return a placeholder
                return "Unknown timestamp format"
        except Exception as e:
            # If any error occurs, return a placeholder
            return f"Error processing timestamp: {str(e)}"
    
    def parse_targets(self, input_targets):
        """
        Parse a string or list of targets into a clean list of individual domains/IPs.
        Handles comma-separated, space-separated, or mixed input formats.
        """
        if not input_targets:
            return []
        
        # If input is already a list, join it with commas to standardize processing
        if isinstance(input_targets, list):
            input_str = ",".join(input_targets)
        else:
            input_str = str(input_targets)
        
        # Replace any spaces with commas, then split by comma
        normalized = input_str.replace(" ", ",")
        
        # Split by comma and clean each item
        targets = []
        for item in normalized.split(","):
            item = item.strip()
            if item:  # Only add non-empty items
                targets.append(item)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_targets = [x for x in targets if not (x in seen or seen.add(x))]
        
        return unique_targets
    
    def parse_ticket_id(self, input_ticket_id) -> int:
        """Parses a ConnectWise ticket ID from a string or integer."""
        if isinstance(input_ticket_id, int):
            return input_ticket_id
        elif isinstance(input_ticket_id, str):
            try:
                return int(input_ticket_id)
            except ValueError:
                self.logger.error(f"Invalid ticket ID format: {input_ticket_id}")
                return None
        else:
            self.logger.error(f"Invalid ticket ID type: {type(input_ticket_id)}")
            return None

    def format_speedtest_table_row(self, metric: str, value: str) -> str:
        """
        Format a speed test result as a markdown table row with proper status styling.
        
        Args:
            metric (str): The speed test metric (e.g., 'download speed', 'upload speed')
            value (str): The speed test value
            
        Returns:
            str: Formatted markdown table row
        """
        # First, extract the numeric value and units for analysis
        numeric_value = 0
        try:
            # Extract numeric part by removing all non-digit characters except decimal point
            numeric_str = ''.join(c for c in value if c.isdigit() or c == '.')
            numeric_value = float(numeric_str) if numeric_str else 0
        except ValueError:
            numeric_value = 0
        
        # Determine status based on the metric
        status = "unknown"
        
        if "download" in metric.lower():
            if numeric_value >= 1000:  # 1 Gbps or higher
                status = "excellent"
            elif numeric_value >= 500:  # 500 Mbps or higher
                status = "good"
            elif numeric_value >= 100:  # 100 Mbps or higher
                status = "fair"
            elif numeric_value >= 25:   # 25 Mbps or higher
                status = "poor"
            else:
                status = "critical"
        elif "upload" in metric.lower():
            if numeric_value >= 500:   # 500 Mbps or higher
                status = "excellent"
            elif numeric_value >= 200:  # 200 Mbps or higher
                status = "good"
            elif numeric_value >= 50:   # 50 Mbps or higher
                status = "fair"
            elif numeric_value >= 10:   # 10 Mbps or higher
                status = "poor"
            else:
                status = "critical"
        elif "ping" in metric.lower() or "latency" in metric.lower():
            if numeric_value <= 20:     # 20ms or lower
                status = "excellent"
            elif numeric_value <= 50:   # 50ms or lower
                status = "good"
            elif numeric_value <= 100:  # 100ms or lower
                status = "fair"
            elif numeric_value <= 200:  # 200ms or lower
                status = "poor"
            else:
                status = "critical"
        elif "provider" in metric.lower() or "jitter" in metric.lower() or "isp" in metric.lower():
            # No status needed for these metrics
            return f"| **{metric.capitalize()}** | `{value}` | - |"
        
        # Status styling with emoji indicators
        status_styles = {
            'excellent': '🟢 **Excellent**',
            'good': '🟡 **Good**',
            'fair': '🟠 **Fair**',
            'poor': '🔴 **Poor**',
            'critical': '⛔ **Critical**',
            'error': '❌ **Error**',
            'unknown': '❓ **Unknown**'
        }
        
        styled_status = status_styles.get(status, status)
        return f"| **{metric.capitalize()}** | `{value}` | {styled_status} |"
        
        
            
    
    def format_ping_result(self, ping_result):
        """
        Format a ping result dictionary into a human-readable string with status indicator.
        
        Args:
            ping_result (dict): Ping result dictionary containing response, status, and time_ms
            
        Returns:
            str: Formatted string with response time and status
        """
        if isinstance(ping_result, dict) and 'status' in ping_result:
            status = ping_result['status']
            response = ping_result.get('response', 'N/A')
            
            # Status emoji indicators
            status_indicators = {
                'excellent': '🟢', # Green - Excellent
                'good': '🟡',      # Yellow - Good
                'fair': '🟠',      # Orange - Fair
                'poor': '🔴',      # Red - Poor
                'critical': '⛔',  # Stop sign - Critical
                'error': '❌',     # X - Error
                'unknown': '❓'    # Question mark - Unknown
            }

            indicator = status_indicators.get(status, '❓')
            return f"{indicator} {response} ({status})"
        else:
            # For backward compatibility with old format
            return str(ping_result)
    
    def format_ping_table_row(self, target, ping_result):
        """
        Format a ping result as a markdown table row with proper status styling.
        
        Args:
            target (str): The target hostname or IP
            ping_result (dict): Ping result dictionary
            
        Returns:
            str: Formatted markdown table row
        """
        if not isinstance(ping_result, dict) or 'status' not in ping_result:
            return f"| **{target}** | `{ping_result}` |"
        
        status = ping_result['status']
        response = ping_result.get('response', 'N/A')
        
        # Status styling with emoji indicators and color words
        status_styles = {
            'excellent': '🟢 **Excellent**',
            'good': '🟡 **Good**',
            'fair': '🟠 **Fair**',
            'poor': '🔴 **Poor**',
            'critical': '⛔ **Critical**',
            'error': '❌ **Error**',
            'unknown': '❓ **Unknown**'
        }
        
        styled_status = status_styles.get(status, status)
        return f"| **{target}** | {response} | {styled_status} |"
    
    def format_with_separator(self, text, target_length=40, separator="-"):
        """Format text with equals signs on both sides to reach target length."""
        text_length = len(text)
        if text_length >= target_length:
            return text  # Already at or exceeding target length
        
        sep_count = target_length - text_length
        left_sep = separator * (sep_count // 2)
        right_sep = separator * (sep_count - (sep_count // 2))
        return f"{left_sep}{text}{right_sep}"
    
    def _add_prefix(self, text, prefix="| "):
        return f"{prefix}{text}"
        
    def _add_suffix(self, text, suffix=" |"):
        return f"{text}{suffix}"
    
    def format_text_with_prefix_suffix(self, text, prefix="| ", suffix=" |"):
        """Format text with a prefix and suffix."""
        return f"{prefix}{text}{suffix}"
    
    def format_diagnostic_message(self, diagnostics):
        """Format diagnostic information as a text message with equal sign formatting."""
        hostname = diagnostics.get('hostname', 'unknown')
        ip_address = diagnostics.get('ip_address', 'unknown')
        last_reboot = self.human_readable_timestamp(diagnostics.get('last_reboot', 'unknown'))
        
        # Format main sections with equals signs
        network_line = f"Network diagnostics -> {hostname}"
        hostname_line = f"Hostname -> {hostname}"
        ip_line = f"IP Address -> {ip_address}"
        reboot_line = f"Last Reboot -> {last_reboot}"
        speed_line = "Speed Test Results: "
        ping_line = "Ping Results:"
        
        # Format sub-items
        speed_items = ""
        for k, v in diagnostics.get('speed_test', {}).items():
            speed_items += f"  ({f'{k}: {v}'})"
        
        ping_items = ""
        for k, v in diagnostics.get('ping_tests', {}).items():
            formatted_result = self.format_ping_result(v)
            ping_items += f"  ({f'{k}: {formatted_result}'})"
        
        # Assemble the message
        msg = (
            f"{network_line}\n\n"
            f"{hostname_line}\n\n"
            f"{ip_line}\n\n"
            f"{reboot_line}\n\n"
            f"{speed_line}\n\n"
            f"[{speed_items}]"
            f"{ping_line}\n\n"
            f"[{ping_items}]"
        )
        
        return msg
    
    def format_diagnostic_message_markdown(self, diagnostics):
        """Format diagnostic information as a nicely formatted Markdown document."""
        hostname = diagnostics.get('hostname', 'unknown')
        ip_address = diagnostics.get('ip_address', 'unknown')
        last_reboot = self.human_readable_timestamp(diagnostics.get('last_reboot', 'unknown'))
        
        # Create a markdown-formatted message
        msg = (
            f"**Network Diagnostics Report** -> *{hostname}*\n\n"
            f"**System Information**\n\n"
            f"| Parameter | Value |\n"
            f"|-----------|-------|\n"
            f"| **Hostname** | `{hostname}` |\n"
            f"| **IP Address** | `{ip_address}` |\n"
            f"| **Last Reboot** | `{last_reboot}` |\n\n"
        )
        
        # Add speed test results section
        speed_test = diagnostics.get('speed_test', {})
        if speed_test:
            msg += "**Speed Test Results**\n\n"
            msg += "| Metric | Result | Status |\n"
            msg += "|--------|--------|--------|\n"
            for k, v in speed_test.items():
                msg += self.format_speedtest_table_row(k, v) + "\n"
            msg += "\n"
        
        # Add ping results section with status column
        ping_tests = diagnostics.get('ping_tests', {})
        if ping_tests:
            msg += "**Ping Results**\n\n"
            msg += "| Target | Response Time | Status |\n"
            msg += "|--------|--------------|--------|\n"
            for k, v in ping_tests.items():
                msg += self.format_ping_table_row(k, v) + "\n"
            msg += "\n"
        
        temp_time = self.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_time = self.human_readable_timestamp(temp_time)
        msg += f"---\n**Report generated at** *{self.human_readable_timestamp(current_time)}**"
        
        return msg
    