from dotenv import load_dotenv 
from requests.auth import HTTPBasicAuth
from src.utils import logger_utils
import requests
import os

import logging

# Inicializamos el logger
logger_utils.setup_logging()
logger = logging.getLogger(__name__)

# Inicializamos las variables de entorno
load_dotenv() 

class HttpConnector:
    def __init__(self, user, token, url):
        self.user = user
        self.token = token
        self.url = url
    
    def call_repositories_api(self, resource):
        basic = HTTPBasicAuth(self.user, self.token)
        is_proxy_enabled = os.getenv("HTTP_PROXY")
        try:
            # Delete HTTP Warnings
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            if is_proxy_enabled != 'false':
                proxies = {
                    'http': os.getenv("HTTP_PROXY_NAME"),
                    'https': os.getenv("HTTPS_PROXY_NAME"),
                }
                response = requests.get(self.url + resource, auth=basic, proxies=proxies, verify=False, timeout=3)
            else:
                response = requests.get(self.url + resource, auth=basic, verify=False, timeout=5)
            return response
        except requests.exceptions.Timeout:
            response.status_code = "Time Out"
            logger.error(response.status_code)
        except requests.exceptions.ConnectionError:
            response.status_code = "Connection refused"
            logger.error(response.status_code)
    