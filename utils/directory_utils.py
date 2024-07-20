import os
import logging
from utils import basic_utils
from utils.logger_config import LoggerConfig as log_config


log_config.setup_logging()
logger = logging.getLogger(__name__)

def create_dirs(path):
    os.mkdir(path)

def check_dirs(path):
    return os.path.exists(path)

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