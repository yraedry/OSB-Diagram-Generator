from interfaces.file_interface import FileInterface
from utils import directory_utils


class FileRepository(FileInterface):
    def __init__(self, path_dir):
        self.path_dir = path_dir
        
    def get_content_file(self, path, file_name):
        components = directory_utils.get_content_file(path, file_name)
        return components
    
   