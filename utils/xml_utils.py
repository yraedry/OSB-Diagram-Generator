import logging
import xml.etree.ElementTree as ET
from utils.logger_config import LoggerConfig as log_config
from utils import basic_utils
from repository.file_repository import FileRepository
from repository.xml_repository import XmlRepository

log_config.setup_logging()
logger = logging.getLogger(__name__)

class ProxyXmlContent:
    def find_invoke(self, xml_content):
        try:
            get_invoke = ET.fromstring(xml_content).find(".//{*}invoke")
            pipeline_path_name = get_invoke.attrib['ref']
        except AttributeError:
            logger.error("proxy invoke not found")
        return f'{pipeline_path_name}.pipeline'
    
class PipelineXmlContent:
    def find_pipeline_service(self, xml_content):
        try:
            get_services = basic_utils.remove_duplicate_items_xml(ET.fromstring(xml_content).findall(".//{*}service"))
        except AttributeError:
            logger.error("pipeline service not found")
        return get_services

    def find_pipeline_jms_type(self, xml_content):
        try:
            get_jms_types = ET.fromstring(xml_content).findall(".//{*}header[@name='JMSType']/{*}xqueryText")
        except AttributeError:
            logger.error("no jms types found")
        return get_jms_types

class BusinessXmlContent:
    def find_workmanager(self, xml_content):
        try:
            get_values = ET.fromstring(xml_content).find(".//{*}dispatch-policy")
        except AttributeError:
            logger.error("workmanager not found")
        return get_values
    
class XmlCommonContent:
    def find_type(self, xml_content):
        common_type = ET.fromstring(xml_content).find(".//{*}provider-id")
        common_type_value = common_type.text
        try:
            if common_type_value == "jms":
                common_type = ET.fromstring(xml_content).find(".//{*}message-selector")
                common_type_value = common_type.text
        except AttributeError:
            logger.info("type not found")
        return common_type_value
    
    def find_uri(self, xml_content):
        try:
            common_uri = ET.fromstring(xml_content).find(".//{*}value")
            common_uri_value = common_uri.text
        except (AttributeError, UnboundLocalError):
            common_uri_value = "not found"
            logger.error("uri not found")
        return common_uri_value
class XmlCommons:
    def get_xml_values(self, repo, file_type, xml_repository: XmlRepository, file_repository: FileRepository):
        xml_content = {}
        xml_path = xml_repository.get_path(repo, file_type)
        xml_name = xml_repository.get_file_path(xml_path, file_type)
        for content in xml_name:
            xml_content[content] = file_repository.get_content_file(xml_path, content)
        return xml_content