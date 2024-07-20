import logging
import logging.config
from datetime import datetime

CONFIG_DIR = "./properties"
LOG_DIR = "./logs"
ENV = 'dev'

class LoggerConfig:
    def setup_logging():
        """Load logging configuration"""
        # log_configs = {"dev": "logger.ini", "prod": "logging.prod.ini"}
        log_configs = {"dev": "logger.conf"}
        config = log_configs.get(ENV, "logger.conf")
        config_path = "/".join([CONFIG_DIR, config])

        # timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")
        timestamp = datetime.now().strftime("%Y.%m.%d")

        logging.config.fileConfig(
            config_path,
            disable_existing_loggers=False,
            defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
        )