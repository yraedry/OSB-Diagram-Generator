import logging
import xml.etree.ElementTree as ET
from utils.logger_config import LoggerConfig as log_config
from utils import basic_utils

log_config.setup_logging()
logger = logging.getLogger(__name__)

def find_proxy_invoke(xml_content):
    try:
        get_invoke = ET.fromstring(xml_content).find(".//{*}invoke")
        pipeline_path_name = get_invoke.attrib['ref']
    except:
        logger.error("no pipeline found")
    return f'{pipeline_path_name}.pipeline'

def find_proxy_type(xml_content):
    proxy_type = ET.fromstring(xml_content).find(".//{*}provider-id")
    proxy_type_text = proxy_type.text
    try:
        if proxy_type_text == "jms":
            proxy_type = ET.fromstring(xml_content).find(".//{*}message-selector")
            proxy_type_text = proxy_type.text
    except:
        logger.info("no proxy type found")
    return proxy_type

def find_pipeline_service(xml_content):
    try:
        get_services = basic_utils.remove_duplicate_items_xml(ET.fromstring(xml_content).findall(".//{*}service"))
    except:
        logger.error("no service found")
    return get_services

def find_pipeline_jms_type(xml_content):
    try:
        get_jms_types = ET.fromstring(xml_content).findall(".//{*}header[@name='JMSType']/{*}xqueryText")
    except:
        logger.error("no jms types found")
    return get_jms_types

def find_business_values(xml_content):
    try:
        get_values = ET.fromstring(xml_content).find(".//{*}value")
    except:
        logger.error("no business values found")
    return get_values