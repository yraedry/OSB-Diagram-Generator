from interfaces.business_interface import BusinessInterface
from utils.xml_utils import XmlCommonContent

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
    def __init__(self, pipeline_name_relation, business_name, uri):
        self.pipeline_name_relation = pipeline_name_relation
        self.business_name = business_name
        self.uri = uri

    