from src.services.interfaces.osb_interface import OsbInterface
from src.utils import logger_utils
from src.utils import basic_utils
import logging

# Inicializamos el logger
logger_utils.setup_logging()
logger = logging.getLogger(__name__)


class OsbOperations(OsbInterface):
    def get_project_name(self, project_name):
        return project_name
    
    def get_proxy_service(self, proxy_service):
        return proxy_service
    
    def get_pipeline(self, pipeline):
        return pipeline
    
    def get_business_service(self, business_service):
        return business_service
    

class OsbProject():
    def __init__(self, project):
        self.project = project
    
    def add_project_name(self, project_name):
        self.project_name = project_name
        return project_name
    
    def create_osb_object(self, osb_components_lists):
        pattern = r'JMSType = '
        project = []
        delete_indexs = []
        no_relation_proxy_indexs = []
        for osb_components in osb_components_lists:
            if osb_components_lists.index(osb_components) not in delete_indexs:
                no_relation_proxy_indexs.append(osb_components_lists.index(osb_components))
            for osb_component in osb_components_lists:
                if len(osb_components.pipeline.associated_jms_components) > 0:
                    if basic_utils.delete_with_pattern(pattern, osb_component.proxy_type) in osb_components.pipeline.associated_jms_components[osb_components.proxy_name]:
                        osb_components.pipeline.proxy_service.append(osb_component)
                        if osb_components_lists.index(osb_component) not in delete_indexs:
                            delete_indexs.append(osb_components_lists.index(osb_component))
        no_relation_proxy_indexs = list(set(no_relation_proxy_indexs).difference(delete_indexs))
        for no_relation_proxy_index in no_relation_proxy_indexs:
            project.append(osb_components_lists[no_relation_proxy_index])
        return project