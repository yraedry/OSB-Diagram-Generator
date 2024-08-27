from interfaces.business_interface import BusinessInterface
from utils.xml_utils import XmlCommonContent
from utils.xml_utils import XmlCommons
from repository.xml_repository import XmlRepository
from repository.file_repository import FileRepository

class BusinessRepository(BusinessInterface):
    def get_name(self, business_name):
        return business_name
    
    def get_uri(self, business_file):
        common_content = XmlCommonContent()
        business_uri = common_content.find_uri(business_file)
        return business_uri
    
    def get_type(self, business_file):
        common_content = XmlCommonContent()
        business_type = common_content.find_type(business_file)
        return business_type
        
class BusinessService:
    def __init__(self, pipeline_name_relation, business_name, business_uri, business_type):
        self.pipeline_name_relation = pipeline_name_relation
        self.business_name = business_name
        self.business_uri = business_uri
        self.business_type = business_type
    
    def create_business_object(self, repo, path, pipeline_name, business_child_name):
        business_repository = BusinessRepository()
        xml_commons = XmlCommons()
        xml_repository = XmlRepository(path)
        file_repository = FileRepository(path)
        file_type = 'bix'
        business_content = xml_commons.get_xml_values(repo, file_type, xml_repository, file_repository)
        business_name = business_repository.get_name(business_child_name)
        if business_child_name not in business_content:
            external_dependency = 'external dependency'
            business_type =  external_dependency
            business_uri = external_dependency
        else:
            business_type = business_repository.get_type(business_content[business_child_name])
            business_uri = business_repository.get_uri(business_content[business_child_name])
        business = BusinessService(pipeline_name, business_name, business_uri, business_type)
        return business
        
    def add_business_to_pipeline(self, pipeline, business_service):
        pipeline.add_business(business_service)
        return pipeline
    