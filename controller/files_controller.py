from utils.properties_operations import PropertyOperations as property_config
from utils.logger_config import LoggerConfig as log_config
import logging
from utils import basic_utils
from utils import directory_utils
import os

log_config.setup_logging()
logger = logging.getLogger(__name__)

class FilesController:
    def __init__(self, path_dir):
        self.path_dir = path_dir

    def get_repositories_path(self):
        osb_services_list = []
        service_dir = os.path.normpath(f'{self.path_dir}/files/services.txt')
        osb_dir = os.path.normpath(f'{self.path_dir}/cloned_repositories')
        osb_services = open(service_dir, "r")
        for service in osb_services:
            osb_services_list.append(f'{osb_dir}{service.replace("\n", "")}')
        return osb_services_list

    def get_proxy_path(self, repo):
        repository_path = os.path.normpath(f'{self.path_dir}/cloned_repositories\{repo}')
        proxy_path = directory_utils.get_folder_path('proxy')
        return proxy_path

    def get_pipeline_path(self, repo):
        repository_path = os.path.normpath(f'{self.path_dir}/cloned_repositories/{repo}')
        pipeline_path = directory_utils.get_folder_path('pipeline')
        return pipeline_path
    
    def get_business_path(self, repo):
        repository_path = os.path.normpath(f'{self.path_dir}/cloned_repositories/{repo}')
        business_path = directory_utils.get_folder_path('bix')
        return business_path
    
    def get_file_from_path(self, path, file_type):
        components = directory_utils.get_file_name(file_type)
        return components
