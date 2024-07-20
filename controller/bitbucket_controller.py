from utils.properties_operations import PropertyOperations as property_config
from utils.logger_config import LoggerConfig as log_config
import requests
from requests.auth import HTTPBasicAuth
import logging
from utils import basic_utils

log_config.setup_logging()
logger = logging.getLogger(__name__)

class BitBucketController:
    def __init__(self, url):
        self.url = url
    
    def call_bitbucket_api(self, url):
        basic = HTTPBasicAuth(property_config.read_properties('CredentialSection', 'credential.user'), property_config.read_properties('CredentialSection', 'credential.tokenApi'))
        is_proxy_enabled = property_config.read_properties('ProxySection', 'proxy.enabled')
        try:
            # Delete HTTP Warnings
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            if is_proxy_enabled != 'false':
                proxies = {
                    'http': property_config.read_properties('ProxySection', 'proxy.http'),
                    'https': property_config.read_properties('ProxySection', 'proxy.https')
                }
                response = requests.get(self.url + url, auth=basic, proxies=proxies, verify=False, timeout=3).json()
            else:
                response = requests.get(self.url + url, auth=basic, verify=False, timeout=5).json()
            return response
        except requests.exceptions.Timeout:
            response.status_code = "Time Out"
            logger.error(response.status_code)
        except requests.exceptions.ConnectionError:
            response.status_code = "Connection refused"
            logger.error(response.status_code)
            
    def get_bitbucket_repos(self):
        response_api = self.call_bitbucket_api(f'?limit={property_config.read_properties('BitbucketSection', 'bitbucket.param')}')
        return response_api

    def get_bitbucket_files(self, repo):
        response_api = self.call_bitbucket_api(f'/{repo}/files?limit=20000')
        return response_api

    def get_bitbucket_component(self, repo, component):
        response_api = self.call_bitbucket_api(f'/{repo}/browse/{component}?limit=20000')
        try:
            if response_api['isLastPage'] is not True:
                second_api_request = self.call_bitbucket_api(f'/{repo}/browse/{component}?start={response_api['nextPageStart']}&limit=20000')
                second_response_to_xml = basic_utils.response_json_to_xml(second_api_request)
                response_api = f'{response_api}{second_response_to_xml}'
        except:
            logger.error('found error in service, continue with errors')
        return response_api
