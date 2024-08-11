from interfaces.proxy_interface import ProxyInterface
from utils.xml_utils import ProxyXmlContent, XmlCommonContent
from utils.xml_utils import XmlCommons
from repository.xml_repository import XmlRepository
from repository.file_repository import FileRepository
from utils import basic_utils
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
    
    def create_all_proxy_object(self, repo, path):
        proxy_repository = ProxyRepository()
        xml_commons = XmlCommons()
        xml_repository = XmlRepository(path)
        file_repository = FileRepository(path)
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
    
    def create_proxy_object(self, repo, path, proxy_child_name):
        proxy_repository = ProxyRepository()
        xml_commons = XmlCommons()
        xml_repository = XmlRepository(path)
        file_repository = FileRepository(path)
        file_type = 'proxy'
        proxy_content = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        proxy_name = proxy_repository.get_name(proxy_child_name)
        if proxy_child_name not in proxy_content:
            external_dependency = 'external dependency'
            proxy_type = external_dependency
            associated_pipeline =  external_dependency
            proxy_uri = external_dependency
        else:
            proxy_type = proxy_repository.get_type(proxy_content[proxy_child_name])
            associated_pipeline =  basic_utils.get_last_part_value_from_character('/',proxy_repository.get_invoke(proxy_content[proxy_child_name]))
            proxy_uri = proxy_repository.get_uri(proxy_content[proxy_child_name])
        proxy = ProxyService(proxy_name, proxy_uri, proxy_type, associated_pipeline)
        
        return proxy

    def add_pipeline(self, child_pipeline):
        self.pipeline = child_pipeline        
        
    def add_pipeline_to_proxy(self, proxy_service, pipeline):
        proxy_service.add_pipeline(pipeline)
        return proxy_service
    
    def add_proxy_to_pipeline(self, pipeline, proxy_service):
        pipeline.add_proxy(proxy_service)
        return pipeline
