from interfaces.pipeline_interface import PipelineInterface
from utils.xml_utils import PipelineXmlContent
from repository.business_repository import BusinessService

class PipelineRepository(PipelineInterface):
    def get_name(self, pipeline_name):
        return pipeline_name
    
    def get_service(self, pipeline_file):
        osb_pipeline = PipelineXmlContent()
        service = osb_pipeline.find_pipeline_service(pipeline_file)
        return service
        
class Pipeline:
    def __init__(self, proxy_name_relation, pipeline_name):
        self.proxy_name_relation = proxy_name_relation
        self.pipeline_name = pipeline_name
        self.business_service = []
    
    def add_business(self, child_business: BusinessService):
        self.business_service.append(child_business)