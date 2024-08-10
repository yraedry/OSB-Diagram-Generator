from utils.properties_operations import PropertyOperations as property_config
from utils import basic_utils
from repository.proxy_repository import ProxyRepository, ProxyService
from repository.pipeline_repository import PipelineRepository, Pipeline
from repository.business_repository import BusinessRepository, BusinessService
from utils.xml_utils import XmlCommons
from utils.logger_config import LoggerConfig as log_config
from services.osb_diagram_services import OsbDiagramService
import logging
from repository.xml_repository import XmlRepository
from repository.file_repository import FileRepository

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbLocalReposService:
    def __init__(self, path):
        self.path = path
        
    def create_components_relation(self, components) -> None:
        proxies_list = []
        services = Services(self.path)
        repository = services.get_service_name(components)
        proxies_list = self.create_proxy_object(repository)
        for proxy_value in proxies_list:
            pipelines_list = (self.create_pipeline_object(repository, proxy_value.proxy_name))
            for pipeline_value in pipelines_list:
                if pipeline_value.pipeline_name == proxy_value.pipeline_relation:
                    self.add_pipeline_to_proxy(proxy_value, pipelines_list)

    def create_proxy_object(self, repo):
        proxy_repository = ProxyRepository()
        xml_commons = XmlCommons()
        xml_repository = XmlRepository(self.path)
        file_repository = FileRepository(self.path)
        proxy_service_list = []
        file_type = 'proxy'
        proxy_content = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        for xml_values in proxy_content:
            proxy_name = proxy_repository.get_name(xml_values)
            proxy_type = proxy_repository.get_type(proxy_content[xml_values])
            associated_pipeline =  basic_utils.get_last_part_value_from_character('/',proxy_repository.get_invoke(proxy_content[xml_values]))
            proxy_uri = proxy_repository.get_uri(proxy_content[xml_values])
            proxy = ProxyService(proxy_name, proxy_uri, proxy_type, associated_pipeline)
            proxy_service_list.append(proxy)
        return proxy_service_list
    
    
    def create_pipeline_object(self, repo, proxy_name):
        pipeline_repository = PipelineRepository()
        xml_commons = XmlCommons()
        xml_repository = XmlRepository(self.path)
        file_repository = FileRepository(self.path)
        pipeline_list = []
        proxy_keys_list = []
        exclude_services= basic_utils.create_list_from_properties(property_config.read_properties('services', 'exclude'))
        pipeline_service_relations = []
        file_type = 'pipeline'
        pipeline_content = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        for xml_values in pipeline_content:
            pipeline_services = pipeline_repository.get_service(pipeline_content[xml_values])
            for key in pipeline_services.keys():
                if key not in proxy_keys_list:
                    proxy_keys_list.append(key)
        for pipeline_key in pipeline_services:
            if basic_utils.get_file_name(pipeline_key) not in exclude_services:
                if 'ProxyRef' in pipeline_services[pipeline_key]:
                    pipeline_service_relations.append(f'{pipeline_key}.proxy')
                elif 'BusinessServiceRef' in pipeline_services[pipeline_key]:
                    pipeline_service_relations.append(f'{pipeline_key}.bix')
        pipeline_name = pipeline_repository.get_name(xml_values)
        pipeline = Pipeline(proxy_name, pipeline_name, pipeline_service_relations)
        pipeline_list.append(pipeline)
        return pipeline_list
    
    def create_business_object(self, repo, pipeline_name):
        business_repository = BusinessRepository()
        xml_commons = XmlCommons()
        xml_repository = XmlRepository(self.path)
        file_repository = FileRepository(self.path)
        business_service_list = []
        file_type = 'bix'
        business_content = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        for xml_values in business_content:
            business_name = business_repository.get_name(pipeline_name)
            business_type = business_repository.get_type(business_content[xml_values])
            business_uri = business_repository.get_uri(business_content[xml_values])
            business = BusinessService(business_name, business_type, business_uri)
            business_service_list.append(business)
        return business_service_list
    
    def add_pipeline_to_proxy(self, proxy_service: ProxyService, pipeline: Pipeline):
        proxy_service.add_pipeline(pipeline)
        return proxy_service
    

class Services(OsbLocalReposService):
    def get_services_files(self) -> None:
        service_files_repo=[]
        xml_repository = XmlRepository(self.path)
        service_files_repo = xml_repository.get_path_repositories()
        self.create_components_relation(service_files_repo)

    def get_service_name(self, components):
        for component in components:
            repo = basic_utils.get_last_part_value_from_character('\\', component)
        return repo

    
        
 