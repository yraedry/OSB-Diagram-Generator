from interfaces.osb_interface import OsbInterface
from repository.proxy_repository import ProxyService
from repository.pipeline_repository import  Pipeline
from repository.business_repository import BusinessService
from utils.logger_config import LoggerConfig as log_config
from utils import basic_utils
import logging
# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)


class OsbRepository(OsbInterface):
    def get_project_name(self, project_name):
        return project_name
    
    def get_proxy_service(self, proxy_service):
        return proxy_service
    
    def get_pipeline(self, pipeline):
        return pipeline
    
    def get_business_service(self, business_service):
        return business_service
    

class OsbProject(ProxyService, Pipeline, BusinessService):
    def __init__(self, project_name, proxy_service, pipeline, business_service):
        self.project_name = project_name
        self.proxy_service = proxy_service
        self.pipeline = pipeline
        self.business_service = business_service
    
    def add_project_name(self, project_name):
        self.project_name = project_name
        return project_name
     
    def add_proxy(self, proxy_service):
        self.proxy_service = proxy_service
        return proxy_service
    
    def add_pipeline(self, pipeline):
        self.pipeline = pipeline
        return pipeline
    
    def add_business(self, business_service):
        self.business_service = business_service
        return business_service
    
    def find_relations(self, proxy_services):
        pattern = r'JMSType = '
        for proxy_service in proxy_services:
            for find_relation in proxy_services:
                if basic_utils.delete_with_pattern(pattern, find_relation.proxy_type) in proxy_service.pipeline.associated_components[proxy_service.proxy_name]:
                    logger.info('encontrada relacion')
                    proxy_service.pipeline.proxy_service.append(find_relation)
                    # cada vez que encuentre algun hijo hay que eliminarlo de la lista y hay que añadir los business_Services
        logger.info('finalizado')
