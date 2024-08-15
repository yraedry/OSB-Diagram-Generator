from interfaces.pipeline_interface import PipelineInterface
from utils.xml_utils import PipelineXmlContent
from repository.osb_repository import OsbRepository
from utils.xml_utils import XmlCommons
from repository.xml_repository import XmlRepository
from repository.file_repository import FileRepository
from utils import basic_utils
from utils.properties_operations import PropertyOperations as property_config
from utils.logger_config import LoggerConfig as log_config
import logging

log_config.setup_logging()
logger = logging.getLogger(__name__)
class PipelineRepository(PipelineInterface):
    def get_name(self, pipeline_name):
        return pipeline_name
    
    def get_service(self, pipeline_file):
        osb_pipeline = PipelineXmlContent()
        service = osb_pipeline.find_pipeline_service(pipeline_file)
        return service
        
class Pipeline(OsbRepository):
    def __init__(self, proxy_name_relation, pipeline_name):
        self.proxy_name_relation = proxy_name_relation
        self.pipeline_name = pipeline_name
        self.proxy_service = []
        self.associated_components = {}
        self.business_service = []
    
    def create_pipeline_object(self, repo, path, proxy_name, associated_pipeline):
        pipeline_repository = PipelineRepository()
        xml_commons = XmlCommons()
        xml_repository = XmlRepository(path)
        file_repository = FileRepository(path)
        file_type = 'pipeline'
        pipelines_dict = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        pipeline_services = pipeline_repository.get_service(pipelines_dict[associated_pipeline])
        pipeline_name = pipeline_repository.get_name(associated_pipeline)
        pipeline = Pipeline(proxy_name, pipeline_name)
        pipeline.associated_components = pipeline_services
        return pipeline
    
    def create_jms_pipeline_object(self, repo, path, proxy_name, associated_pipeline):
        pipeline_repository = PipelineRepository()
        xml_commons = XmlCommons()
        osb_pipeline = PipelineXmlContent()
        xml_repository = XmlRepository(path)
        file_repository = FileRepository(path)
        file_type = 'pipeline'
        jms_types_relations = []
        pipelines_dict = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        pipeline_name = pipeline_repository.get_name(associated_pipeline)
        pipeline = Pipeline(proxy_name, pipeline_name)
        check_jms_type = osb_pipeline.find_pipeline_jms_type(pipelines_dict[associated_pipeline])     
        if check_jms_type is not None: 
            for jms_type in check_jms_type:
                jms_types_relations.append(jms_type.text)    
            pipeline.associated_components[proxy_name] = jms_types_relations
        return pipeline

    def add_proxy(self, child_proxy):
        self.proxy_service.append(child_proxy)
        
    def add_business(self, child_business):
        self.business_service.append(child_business)