import os
from utils.properties_operations import PropertyOperations as property_config
from utils import basic_utils
from utils.logger_config import LoggerConfig as log_config
from services.osb_diagram_services import OsbDiagramService
from controller.files_controller import FilesController
import logging
import xml.etree.ElementTree as ET

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbLocalReposService:
    def __init__(self, path):
        self.path = path

    def get_services_files(self):
        service_files_repo=[]
        file_controller = FilesController(os.getcwd())
        service_files_repo = file_controller.get_repositories_path()
        return service_files_repo


