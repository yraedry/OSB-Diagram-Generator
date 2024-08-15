from interfaces.osb_interface import OsbInterface
from utils.xml_utils import ProxyXmlContent, XmlCommonContent
from utils.xml_utils import XmlCommons
from repository.xml_repository import XmlRepository
from repository.file_repository import FileRepository
from utils import basic_utils
from utils.properties_operations import PropertyOperations as property_config

class OsbRepository(OsbInterface):
    def get_project_name(self, project_name):
        return project_name
    
    def get_proxy_service(self, proxy_service):
        return proxy_service
    
    def get_pipeline(self, pipeline):
        return pipeline
    
    def get_business_service(self, business_service):
        return business_service
    

class OsbProject:
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