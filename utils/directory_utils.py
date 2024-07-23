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

def get_folder_path(service_path, search_type):
    folder_path = ''
    directory = service_path
    for path, folders, files in os.walk(directory):
        for file in files:
            extension = basic_utils.get_last_part_value_from_character('.', file)
            if extension == search_type:
                folder_path = path
    return folder_path

def get_file_name(file_path, search_type):
    files_name_list = []
    directory = file_path
    for path, folders, files in os.walk(directory):
        for file in files:
            extension = basic_utils.get_last_part_value_from_character('.', file)
            if extension == search_type:
                files_name_list.append(file)
    return files_name_list

def get_content_file(file_path, file_name):
    with open(os.path.join(file_path, file_name)) as f:
        file_content = f.read()
    return file_content