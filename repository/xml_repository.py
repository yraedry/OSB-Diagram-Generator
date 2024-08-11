import os
from interfaces.xml_interface import XmlInterface
from utils import directory_utils

class XmlRepository(XmlInterface):
    def __init__(self, path_dir):
        self.path_dir = path_dir
        
    def get_path(self, repo, file_type):
        repository_path = os.path.normpath(f'{self.path_dir}/cloned_repositories/{repo}')
        path = directory_utils.get_folder_path(repository_path, file_type)
        return path
    
    def get_file_path(self, path, file_type):
        components = directory_utils.get_file_name(path, file_type)
        return components
    
    def get_content_file_from_path(self, path, file_name):
        components = directory_utils.get_content_file(path, file_name)
        return components
    
    def get_path_repositories(self):
        osb_services_list = []
        service_dir = os.path.normpath(f'{self.path_dir}/files/services.txt')
        osb_dir = os.path.normpath(f'{self.path_dir}/cloned_repositories')
        osb_services = open(service_dir, "r")
        for service in osb_services:
            osb_services_list.append(os.path.normpath(f'{osb_dir}/{service.replace("\n", "")}'))
        return osb_services_list
    
