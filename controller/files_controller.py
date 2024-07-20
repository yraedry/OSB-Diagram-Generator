from utils.properties_operations import PropertyOperations as property_config
from utils.logger_config import LoggerConfig as log_config
import logging
from utils import basic_utils
from services.osb_local_repos_services import OsbLocalReposService
import os

log_config.setup_logging()
logger = logging.getLogger(__name__)

class FilesController:
    def __init__(self, path_dir):
        self.path_dir = path_dir

    def get_repositories_path(self):
        osb_services_list = []
        service_dir = f'{self.path_dir}\\files\\services.txt'
        osb_dir = f'{self.path_dir}\\cloned_repositories\\'
        osb_services = open(service_dir, "r")
        for service in osb_services:
            osb_services_list.append(f'{osb_dir}{service.replace("\n", "")}')
        return osb_services_list

    def get_proxy_path(self, repo):
        repository_path = f'{self.path_dir}\\cloned_repositories\\{repo}'
        osb_local_services = OsbLocalReposService(repository_path)
        proxy_path = osb_local_services.get_folder_path('proxy')
        return proxy_path

    def get_pipeline_path(self, repo):
        repository_path = f'{self.path_dir}\\cloned_repositories\\{repo}'
        osb_local_services = OsbLocalReposService(repository_path)
        pipeline_path = osb_local_services.get_folder_path('pipeline')
        return pipeline_path
    
    def get_business_path(self, repo):
        repository_path = f'{self.path_dir}\\cloned_repositories\\{repo}'
        osb_local_services = OsbLocalReposService(repository_path)
        business_path = osb_local_services.get_folder_path('bix')
        return business_path
    
    def get_file_from_path(self, path, file_type):
        osb_local_services = OsbLocalReposService(path)
        components = osb_local_services.get_file_name(file_type)
        return components
