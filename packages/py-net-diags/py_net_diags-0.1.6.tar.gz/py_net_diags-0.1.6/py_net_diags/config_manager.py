import os
import re
import json
import logging
from dotenv import load_dotenv

LOG = logging.getLogger("py_net_diags.config_manager")

class ConfigManager:
    """Manages configuration settings for ConnectWise API integration."""
    
    def __init__(self, log=None):
        self.log = log if log is not None else LOG
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        """
        _load_config

        Description: Load configuration from environment file.
        """
        try:
            load_dotenv()
            self.config = {
                "base_url": os.getenv("CW_BASE_URL", "https://cw.managedsolution.com/v4_6_release/apis/3.0"),
                "auth": os.getenv("AUTHORIZATION"),
                "client_id": os.getenv("CLIENTID"),
                "retry_attempts": int(os.getenv("RETRY_ATTEMPTS", "5")),
                "retry_delay": int(os.getenv("RETRY_DELAY", "30")),
                "running_in_asio": os.getenv("RUNNING_IN_ASIO", "True").lower() == "true",
            }
            
            # Log masked configuration
            if self.log:
                masked_config = self.config.copy()
                if masked_config.get("auth"):
                    masked_config["auth"] = re.sub(r'(?<=.{8}).', '*', masked_config["auth"])
                if masked_config.get("client_id"):
                    masked_config["client_id"] = re.sub(r'(?<=.{8}).', '*', masked_config["client_id"])
                
                self.log.debug(f"Configuration loaded: {json.dumps(masked_config, indent=2)}")
                
        except Exception as e:
            if self.log:
                self.log.error(f"Failed to load configuration: {str(e)}")
            else:
                print(f"Failed to load configuration: {str(e)}")
    
    def get(self, key, default=None):
        """
        get

        Description: Get configuration value by key.

        Args:
            key (_type_): The key to retrieve.
            default (_type_, optional): the default value to return if the key is not found. (default: None)

        Returns:
            _type_: The configuration value for the given key or the default value if not found.
        """
        return self.config.get(key, default)
