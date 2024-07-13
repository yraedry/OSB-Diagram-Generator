from utils import properties_operations as config
import logging
from utils.logger_config import LoggerConfig as log_config
from controller.bitbucket_controller import BitBucketController
from utils import basic_utils

log_config.setup_logging()
logger = logging.getLogger(__name__)

def main() -> None:
    controller = BitBucketController()
    controller.get_services_files('')
if __name__ == "__main__":
    main()


