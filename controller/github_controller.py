from utils.properties_operations import PropertyOperations as property_config
from utils.logger_config import LoggerConfig as log_config
import requests
from requests.auth import HTTPBasicAuth
import logging
from utils import basic_utils

log_config.setup_logging()
logger = logging.getLogger(__name__)

class GithubtController:
    def __init__(self, url):
        self.url = url
    
    def call_github_api(self, url):
        basic = HTTPBasicAuth(property_config.read_properties('credential', 'user'), property_config.read_properties('credential', 'tokenApi'))
        is_proxy_enabled = property_config.read_properties('proxy', 'enabled')
        try:
            # Delete HTTP Warnings
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            if is_proxy_enabled != 'false':
                proxies = {
                    'http': property_config.read_properties('proxy', 'http'),
                    'https': property_config.read_properties('proxy', 'https')
                }
                response = requests.get(self.url + url, auth=basic, proxies=proxies, verify=False, timeout=3)
            else:
                response = requests.get(self.url + url, auth=basic, verify=False, timeout=5)
            return response
        except requests.exceptions.Timeout:
            response.status_code = "Time Out"
            logger.error(response.status_code)
        except requests.exceptions.ConnectionError:
            response.status_code = "Connection refused"
            logger.error(response.status_code)
    
    def get_all_github_repos(self):
        github_repositories = self.call_github_api(f'/users/{property_config.read_properties('credential', 'user')} /repos')
        return github_repositories

    def get_github_repo(self, repo):
        github_repository = self.call_github_api(f'/repos/{property_config.read_properties('credential', 'user')}/{repo}/contents')
        return github_repository
    
    def get_github_files(self, repo, content):
        github_files = self.call_github_api(f'/repos/{property_config.read_properties('credential', 'user')}/{repo}/contents/{content}')
        return github_files
    
    def get_github_content_file(self, repo, folder_content, resource):
        github_file_content = self.call_github_api(f'/{property_config.read_properties('credential', 'user')}/{repo}/{property_config.read_properties('github', 'branch')}/{folder_content}/{resource}')
        return github_file_content