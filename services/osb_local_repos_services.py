from utils.properties_operations import PropertyOperations as property_config
from utils import basic_utils
from repository.proxy_repository import ProxyService
from repository.pipeline_repository import  Pipeline
from utils.logger_config import LoggerConfig as log_config
from services.osb_diagram_services import OsbDiagramService
import logging
from repository.xml_repository import XmlRepository

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbLocalReposService:
    def __init__(self, path):
        self.path = path
        
    def create_components_relation(self, components) -> None:
        proxies_list = []
        include_jms_proxies = False
        services = Services(self.path)
        proxy_services = ProxyService('','','','')
        pipeline = Pipeline('','')
        repository = services.get_service_name(components)
        proxies_list = proxy_services.create_all_proxy_object(repository, self.path)
        if proxies_list[1] == True:
            include_jms_proxies = True
        for proxy_value in proxies_list[0]:
            if include_jms_proxies == False:
                pipeline = pipeline.create_pipeline_object(repository, self.path, proxy_value.proxy_name, proxy_value.pipeline_relation)
            else:
                pipeline = pipeline.create_jms_pipeline_object(repository, self.path, proxy_value.proxy_name, proxy_value.pipeline_relation)
            if pipeline.pipeline_name == proxy_value.pipeline_relation:
                    proxy_services.add_pipeline_to_proxy(proxy_value, pipeline)
        logger.info('objeto terminado')


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

    
        
 