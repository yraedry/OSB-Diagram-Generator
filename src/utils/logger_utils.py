import logging
import logging.config
from datetime import datetime

CONFIG_DIR = "./src/logs/properties"
LOG_DIR = "./src/logs/files"
ENV = 'dev'

def setup_logging():
    # Configuracion del logger
    log_configs = {"dev": "logger.ini"}
    config = log_configs.get(ENV, "logger.ini")
    config_path = "/".join([CONFIG_DIR, config])
    timestamp = datetime.now().strftime("%Y.%m.%d")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
    )