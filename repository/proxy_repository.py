from interfaces.proxy_interface import ProxyInterface
from utils.xml_utils import ProxyXmlContent, XmlCommonContent
from repository.pipeline_repository import Pipeline

class ProxyRepository(ProxyInterface):
    def get_name(self, proxy_name):
        return proxy_name
    
    def get_invoke(self, proxy_file):
        osb_proxy = ProxyXmlContent()
        invoke = osb_proxy.find_invoke(proxy_file)
        return invoke
    
    def get_type(self, proxy_file):
        common_content = XmlCommonContent()
        proxy_type = common_content.find_type(proxy_file)
        return proxy_type
    
    def get_uri(self, proxy_file):
        common_content = XmlCommonContent()
        proxy_uri = common_content.find_uri(proxy_file)
        return proxy_uri
        
class ProxyService:
    def __init__(self, proxy_name, uri, proxy_type, pipeline_relation):
        self.proxy_name = proxy_name
        self.uri = uri
        self.proxy_type = proxy_type
        self.pipeline_relation = pipeline_relation
        self.pipeline = []
    
    def add_pipeline(self, child_pipeline: Pipeline):
        self.pipeline = child_pipeline
        
        
