from dotenv import load_dotenv 
from src.utils import logger_utils
from src.services.connectors.http_connector import HttpConnector;
import os
import logging 

# Inicializamos el logger
logger_utils.setup_logging()
logger = logging.getLogger(__name__)

# Inicializamos las variables de entorno
load_dotenv() 

class GithubApi:
    def __init__(self, url):
        self.url = url
    
    def get_all_github_repos(self):
        http_connector = HttpConnector(os.getenv("GITHUB_USER"), os.getenv("GITHUB_TOKEN"), self.url)
        github_repositories = http_connector.call_repositories_api(f'/search/repositories?q=user:{os.getenv("GITHUB_USER")}')
        return github_repositories

    def get_github_repo(self, repo):
        http_connector = HttpConnector(os.getenv("GITHUB_USER"), os.getenv("GITHUB_TOKEN"), self.url)
        github_repository = http_connector.call_repositories_api(f'/repos/{os.getenv("GITHUB_USER")}/{repo}/contents')
        return github_repository
    
    def get_github_files(self, repo, content):
        http_connector = HttpConnector(os.getenv("GITHUB_USER"), os.getenv("GITHUB_TOKEN"), self.url)
        github_files = http_connector.call_repositories_api(f'/repos/{os.getenv("GITHUB_USER")}/{repo}/contents/{content}')
        return github_files
    
    def get_github_content_file(self, repo, folder_content, resource):
        http_connector = HttpConnector(os.getenv("GITHUB_USER"), os.getenv("GITHUB_TOKEN"), self.url)
        github_file_content = http_connector.call_repositories_api(f'/{os.getenv("GITHUB_USER")}/{repo}/{os.getenv("GITHUB_BRANCH")}/{folder_content}/{resource}')
        return github_file_content