from src.utils import basic_utils
from dotenv import load_dotenv 
from src.utils import logger_utils
from src.services.connectors.http_connector import HttpConnector;
import logging
import os

# Inicializamos el logger
logger_utils.setup_logging()
logger = logging.getLogger(__name__)

# Inicializamos las variables de entorno
load_dotenv() 

class BitBucketRoutes:
    def __init__(self, url):
        self.url = url
    
    def get_bitbucket_repos(self):
        http_connector = HttpConnector(os.getenv("BITBUCKET_USER"), os.getenv("BITBUCKET_TOKEN"), self.url)
        response_api = http_connector.call_repositories_api(f'?limit={os.getenv("BITBUCKET_PARAM")}')
        return response_api

    def get_bitbucket_files(self, repo):
        http_connector = HttpConnector(os.getenv("BITBUCKET_USER"), os.getenv("BITBUCKET_TOKEN"), self.url)
        response_api = http_connector.call_repositories_api(f'/{repo}/files?limit=20000')
        return response_api

    def get_bitbucket_component(self, repo, component):
        http_connector = HttpConnector(os.getenv("BITBUCKET_USER"), os.getenv("BITBUCKET_TOKEN"), self.url)
        response_api = http_connector.call_repositories_api(f'/{repo}/browse/{component}?limit=20000')
        try:
            if response_api['isLastPage'] is not True:
                second_api_request = http_connector.call_repositories_api(f'/{repo}/browse/{component}?start={response_api['nextPageStart']}&limit=20000')
                second_response_to_xml = basic_utils.response_json_to_xml(second_api_request)
                response_api = f'{response_api}{second_response_to_xml}'
        except:
            logger.error('found error in service, continue with errors')
        return response_api
