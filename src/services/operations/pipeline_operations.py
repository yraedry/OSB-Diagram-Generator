from src.services.interfaces.pipeline_interface import PipelineInterface
from src.utils.xml_utils import PipelineXmlContent
from src.utils.xml_utils import XmlCommons
from src.services.operations.xml_operations import XmlOperations
from src.services.operations.file_operations import FileOperations
from src.services.operations.proxy_operations import ProxyServiceLocal
from src.services.operations.business_operations import BusinessServiceLocal 
from src.utils import logger_utils
from src.utils import basic_utils
import logging

# Inicializamos el logger
logger_utils.setup_logging()
logger = logging.getLogger(__name__)

class PipelineOperations(PipelineInterface):
    def get_name(self, pipeline_name):
        return pipeline_name
    
    def get_service(self, pipeline_file):
        osb_pipeline = PipelineXmlContent()
        service = osb_pipeline.find_pipeline_service(pipeline_file)
        return service
        
class PipelineLocal:
    def __init__(self, proxy_name_relation, pipeline_name):
        self.proxy_name_relation = proxy_name_relation
        self.pipeline_name = pipeline_name
        self.proxy_service = []
        self.associated_components = {}
        self.associated_jms_components = {}
        self.business_service = []
        self.external_jms_component = []
    
    def create_pipeline_object(self, repo, path, proxy, associated_pipeline):
        pipeline_repository = PipelineOperations()
        xml_commons = XmlCommons()
        osb_pipeline = PipelineXmlContent()
        xml_repository = XmlOperations(path)
        file_repository = FileOperations(path)
        file_type = 'pipeline'
        pipelines_dict = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        check_jms_type = osb_pipeline.find_pipeline_jms_type(pipelines_dict[associated_pipeline])
        if check_jms_type is None or len(check_jms_type) == 0:
            pipeline_services = pipeline_repository.get_service(pipelines_dict[associated_pipeline])
            pipeline_name = pipeline_repository.get_name(associated_pipeline)
            pipeline = PipelineLocal(proxy.proxy_name, pipeline_name)
            pipeline.associated_components = pipeline_services
        else:
            pipeline = self.create_jms_pipeline_object(repo, path, proxy, associated_pipeline)
        return pipeline
    
    def create_jms_pipeline_object(self, repo, path, proxy, associated_pipeline):
        pattern = r'JMSType = '
        pipeline_repository = PipelineOperations()
        xml_commons = XmlCommons()
        osb_pipeline = PipelineXmlContent()
        xml_repository = XmlOperations(path)
        file_repository = FileOperations(path)
        file_type = 'pipeline'
        jms_types_relations = []
        pipelines_dict = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        pipeline_name = pipeline_repository.get_name(associated_pipeline)
        pipeline_services = pipeline_repository.get_service(pipelines_dict[associated_pipeline])
        pipeline = PipelineLocal(proxy.proxy_name, pipeline_name)
        check_jms_type = osb_pipeline.find_pipeline_jms_type(pipelines_dict[associated_pipeline])     
        if check_jms_type is not None: 
            for jms_type in check_jms_type:
                if basic_utils.delete_with_pattern(pattern, proxy.proxy_type) == jms_type.text:
                    proxy.is_recursive = True
                else:
                    jms_types_relations.append(jms_type.text)
            pipeline.associated_components = pipeline_services
            pipeline.associated_jms_components[proxy.proxy_name] = jms_types_relations
        return pipeline

    def add_proxy(self, child_proxy):
        self.proxy_service.append(child_proxy)
        
    def add_business(self, child_business):
        self.business_service.append(child_business)
    
    def add_business_to_pipeline(self, pipeline, associated_component):
        if pipeline.pipeline_name == associated_component.pipeline_name_relation:
            pipeline.add_business(associated_component)
        return pipeline
    
    def add_proxy_to_pipeline(self, pipeline, associated_component):
        pipeline.add_proxy(associated_component)
        return pipeline
    
    def choose_object_to_pipeline(self, pipeline, associated_components):
        for associated_component in associated_components:
            if isinstance(associated_component, BusinessServiceLocal):
                pipeline = self.add_business_to_pipeline(pipeline, associated_component)
            elif isinstance(associated_component, ProxyServiceLocal):
                pipeline = self.add_proxy_to_pipeline(pipeline, associated_component)
        return pipeline
    
class Pipeline:
    def __init__(self, proxy_name_relation, pipeline_name):
        self.proxy_name_relation = proxy_name_relation
        self.pipeline_name = pipeline_name
        self.proxy_service = []
        self.associated_components = {}
        self.associated_jms_components = {}
        self.business_service = []
        self.external_jms_component = []
    
    def create_pipeline_object(self, repo, path, proxy, associated_pipeline):
       pass
    
    def create_jms_pipeline_object(self, repo, path, proxy, associated_pipeline):
        pass


class PipelineCommons(PipelineLocal, Pipeline):  
    def __init__(self, proxy_service, business_service):
        super().__init__(proxy_service, business_service)
        self.proxy_service = proxy_service
        self.business_service = business_service
        
    def add_proxy(self, child_proxy):
        self.proxy_service.append(child_proxy)
        
    def add_business(self, child_business):
        self.business_service.append(child_business)
    
    def add_business_to_pipeline(self, pipeline, associated_component):
        if pipeline.pipeline_name == associated_component.pipeline_name_relation:
            pipeline.add_business(associated_component)
        return pipeline
    
    def add_proxy_to_pipeline(self, pipeline, associated_component):
        pipeline.add_proxy(associated_component)
        return pipeline
    
    def choose_object_to_pipeline(self, pipeline, associated_components):
        for associated_component in associated_components:
            if isinstance(associated_component, BusinessServiceLocal):
                pipeline = self.add_business_to_pipeline(pipeline, associated_component)
            elif isinstance(associated_component, ProxyServiceLocal):
                pipeline = self.add_proxy_to_pipeline(pipeline, associated_component)
        return pipeline