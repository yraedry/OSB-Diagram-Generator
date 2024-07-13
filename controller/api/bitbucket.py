from utils.properties_operations import PropertyOperations as property_config
from utils.logger_config import LoggerConfig as log_config
import requests
from requests.auth import HTTPBasicAuth
import logging

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class BitBucketApi:
    def __init__(self, url):
        self.url = url
    
    def call_bitbucket_api(self, url):
        # Metodo para hacer llamadas a la api de bitbucket de forma generica
        basic = HTTPBasicAuth(property_config.read_properties('CredentialSection', 'credential.user'), property_config.read_properties('CredentialSection', 'credential.tokenApi'))
        proxies = {
            'http': property_config.read_properties('ProxySection', 'proxy.http'),
            'https': property_config.read_properties('ProxySection', 'proxy.https')
        }
        try:
            # Eliminamos el warning HTTP
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(self.url + url, auth=basic, proxies=proxies, verify=False, timeout=3).json()
            return response
        except requests.exceptions.Timeout:
            response.status_code = "Time Out"
            logger.error(response.status_code)
        except requests.exceptions.ConnectionError:
            response.status_code = "Connection refused"
            logger.error(response.status_code)