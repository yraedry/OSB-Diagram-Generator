import os
from src.services.interfaces.xml_interface import XmlInterface
from src.utils import directory_utils

class XmlOperations(XmlInterface):
    def __init__(self, path_dir):
        self.path_dir = path_dir
        
    def get_path(self, repo, file_type):
        repository_path = os.path.normpath("{dir_path}/cloned_repositories/{repository}".format(dir_path = self.path_dir, repository = repo))
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
        service_dir = os.path.normpath('{dir_path}/src/files/services.txt'.format(dir_path = self.path_dir))
        osb_dir = os.path.normpath('{dir_path}/cloned_repositories'.format(dir_path = self.path_dir))
        osb_services = open(service_dir, "r")
        for service in osb_services:
            osb_services_list.append(os.path.normpath('{dir}/{replace_service}'.format(dir = osb_dir, replace_service = service.replace("\n", ""))))
        return osb_services_list
    
