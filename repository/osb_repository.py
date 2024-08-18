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
    def __init__(self, project):
        self.project = project
    
    def add_project_name(self, project_name):
        self.project_name = project_name
        return project_name
    
    def find_relations(self, proxy_services):
        pattern = r'JMSType = '
        project = []
        delete_indexs = []
        no_relation_proxy_indexs = []
        for proxy_service in proxy_services:
            if proxy_services.index(proxy_service) not in delete_indexs:
                no_relation_proxy_indexs.append(proxy_services.index(proxy_service))
            for find_relation in proxy_services:
                if len(proxy_service.pipeline.associated_jms_components) > 0:
                    # bookingJmsMidOffice provoca un loop infinito
                    if basic_utils.delete_with_pattern(pattern, find_relation.proxy_type) in proxy_service.pipeline.associated_jms_components[proxy_service.proxy_name]:
                        proxy_service.pipeline.proxy_service.append(find_relation)
                        if proxy_services.index(find_relation) not in delete_indexs:
                            delete_indexs.append(proxy_services.index(find_relation))
        no_relation_proxy_indexs = list(set(no_relation_proxy_indexs).difference(delete_indexs))
        for no_relation_proxy_index in no_relation_proxy_indexs:
            project.append(proxy_services[no_relation_proxy_index])
        return project
