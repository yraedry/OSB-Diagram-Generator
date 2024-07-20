import os
from utils.properties_operations import PropertyOperations as property_config
from utils import basic_utils
from utils.logger_config import LoggerConfig as log_config
from services.osb_diagram_services import OsbDiagramService
import logging
import xml.etree.ElementTree as ET

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbLocalReposService:
    def __init__(self, path):
        self.path = path


    def get_folder_path(self, search_type):
        folder_path = ''
        directory = self.path
        for path, folders, files in os.walk(directory):
            for file in files:
                extension = basic_utils.get_last_part_value_from_character('.', file)
                logger.debug(extension)
                if extension == search_type:
                    folder_path = path
        return folder_path
    
    def get_file_name(self, search_type):
        files_name_list = []
        directory = self.path
        for path, folders, files in os.walk(directory):
            for file in files:
                extension = basic_utils.get_last_part_value_from_character('.', file)
                logger.debug(extension)
                if extension == search_type:
                    files_name_list.append(file)
        return files_name_list
