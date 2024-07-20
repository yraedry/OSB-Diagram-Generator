import os
from utils.properties_operations import PropertyOperations as property_config
from utils import basic_utils
from controller.bitbucket_controller import BitBucketController
from utils.logger_config import LoggerConfig as log_config
import logging
import xml.etree.ElementTree as ET
from git import Repo

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbJmsService:
    def __init__(self):
        self.repos = ""
       