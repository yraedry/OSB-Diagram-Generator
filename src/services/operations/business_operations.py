from src.services.interfaces.business_interface import BusinessInterface
from src.utils.xml_utils import XmlCommonContent
from src.utils.xml_utils import XmlCommons
from src.services.operations.xml_operations import XmlOperations
from src.services.operations.file_operations import FileOperations

class BusinessOperations(BusinessInterface):
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
        
class BusinessServiceLocal:
    def __init__(self, pipeline_name_relation, business_name, business_uri, business_type):
        self.pipeline_name_relation = pipeline_name_relation
        self.business_name = business_name
        self.business_uri = business_uri
        self.business_type = business_type
    
    def create_business_object(self, repo, path, pipeline_name, business_child_name):
        business_repository = BusinessOperations()
        xml_commons = XmlCommons()
        xml_repository = XmlOperations(path)
        file_repository = FileOperations(path)
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
        business = BusinessServiceLocal(pipeline_name, business_name, business_uri, business_type)
        return business
        
    def add_business_to_pipeline(self, pipeline, business_service):
        pipeline.add_business(business_service)
        return pipeline
    
class BusinessService:
    def __init__(self, pipeline_name_relation, business_name, business_uri, business_type):
        self.pipeline_name_relation = pipeline_name_relation
        self.business_name = business_name
        self.business_uri = business_uri
        self.business_type = business_type
    
    def create_business_object(self, repo, path, pipeline_name, business_child_name):
        pass


class BusinessServiceCommons(BusinessServiceLocal, BusinessService):       
    def add_business_to_pipeline(self, pipeline, business_service):
        pipeline.add_business(business_service)
        return pipeline