from interfaces.pipeline_interface import PipelineInterface
from utils.xml_utils import PipelineXmlContent
from repository.proxy_repository import ProxyService
from repository.business_repository import BusinessService
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
        
class Pipeline(ProxyService, BusinessService):
    def __init__(self, proxy_name_relation, pipeline_name):
        self.proxy_name_relation = proxy_name_relation
        self.pipeline_name = pipeline_name
        self.proxy_service = []
        self.business_service = []
    
    def create_pipeline_object(self, repo, path, proxy_name, associated_pipeline):
        pipeline_repository = PipelineRepository()
        xml_commons = XmlCommons()
        xml_repository = XmlRepository(path)
        file_repository = FileRepository(path)
        exclude_services= basic_utils.create_list_from_properties(property_config.read_properties('services', 'exclude'))
        file_type = 'pipeline'
        pipelines_dict = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        pipeline_services = pipeline_repository.get_service(pipelines_dict[associated_pipeline])
        pipeline_name = pipeline_repository.get_name(associated_pipeline)
        pipeline = Pipeline(proxy_name, pipeline_name)
        for pipeline_key in pipeline_services:
            if basic_utils.get_file_name(pipeline_key) not in exclude_services:
                if 'ProxyRef' in pipeline_services[pipeline_key]:
                    proxy_child = self.create_proxy_object(repo, path, f'{basic_utils.get_last_part_value_from_character('/', pipeline_key)}.proxy')
                    pipeline.add_proxy(proxy_child)
                if 'BusinessServiceRef' in pipeline_services[pipeline_key]:
                    business_child = self.create_business_object(repo, path, associated_pipeline, f'{basic_utils.get_last_part_value_from_character('/', pipeline_key)}.bix')
                    pipeline.add_business(business_child)
        return pipeline
    
    
    def create_jms_pipeline_object(self, repo, path, proxy_name, associated_pipeline):
        pipeline_repository = PipelineRepository()
        xml_commons = XmlCommons()
        osb_pipeline = PipelineXmlContent()
        xml_repository = XmlRepository(path)
        file_repository = FileRepository(path)
        file_type = 'pipeline'
        pipelines_dict = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        pipeline_name = pipeline_repository.get_name(associated_pipeline)
        pipeline = Pipeline(proxy_name, pipeline_name)
        check_jms_type = osb_pipeline.find_pipeline_jms_type(pipelines_dict[associated_pipeline])     
        if check_jms_type is not None: 
            for jms_type in check_jms_type:
                logger.info(jms_type.text)
                # ahora tendriamos que llamar al metodo para generar un objeto proxy de tipo jms con sus hijos correspondientes  
                #le pasaria el nombre del proxy, y ya deberia buscar el la relacion que hay con la lista de proxies                      
        return pipeline

        
        
    def add_proxy(self, child_proxy):
        self.proxy_service.append(child_proxy)
        
    def add_business(self, child_business):
        self.business_service.append(child_business)