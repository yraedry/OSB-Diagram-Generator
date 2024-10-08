from utils.properties_operations import PropertyOperations as property_config
from utils import basic_utils
from repository.osb_repository import OsbProject
from repository.proxy_repository import ProxyService
from repository.pipeline_repository import  Pipeline
from repository.business_repository import BusinessService 
from utils.logger_config import LoggerConfig as log_config
from services.osb_diagram_services import OsbDiagramService
import logging
from repository.xml_repository import XmlRepository

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbLocalReposService:
    def __init__(self, path):
        self.path = path
        
    def create_components_relation(self, components) -> None:
        services = Services(self.path)
        osb_project = OsbProject('')
        proxy_services = ProxyService('','','','')
        pipeline = Pipeline('','')
        repository = services.get_service_name(components)
        osb_project.add_project_name(repository)
        proxies_service_list = proxy_services.create_all_proxy_object(repository, self.path)
        for proxy_value in proxies_service_list:
            if proxy_value.is_jms == False:
                pipeline = pipeline.create_pipeline_object(repository, self.path, proxy_value, proxy_value.pipeline_relation)
            else:
                pipeline = pipeline.create_jms_pipeline_object(repository, self.path, proxy_value, proxy_value.pipeline_relation)
            if pipeline.associated_components is not None:
                associated_components = services.create_child_service_relations(repository, self.path, pipeline)   
            if pipeline.pipeline_name == proxy_value.pipeline_relation:
                pipeline = pipeline.choose_object_to_pipeline(pipeline, associated_components)
            proxy_services.add_pipeline_to_proxy(proxy_value, pipeline)
  
        osb_project.project = osb_project.create_osb_object(proxies_service_list)
        osb_diagram = OsbDiagramService()
        osb_diagram.create_osb_basic_diagram(osb_project)
        return osb_project
    
    def create_project_diagram(self, project):
        osb_project = OsbProject(project)
        OsbDiagramService.create_osb_basic_diagram(osb_project)

class Services(OsbLocalReposService):
    def get_services_files(self) -> None:
        service_files_repo=[]
        xml_repository = XmlRepository(self.path)
        service_files_repo = xml_repository.get_path_repositories()
        self.create_components_relation(service_files_repo)

    def get_service_name(self, components):
        for component in components:
            repo = basic_utils.get_last_part_value_from_character('\\', component)
        return repo

    def create_child_service_relations(self, repo, path, pipeline: Pipeline):
        proxy_services = ProxyService('','','','')
        business_service = BusinessService('','','','')
        associate_component = []
        exclude_services= basic_utils.create_list_from_properties(property_config.read_properties('services', 'exclude'))
        for pipeline_key in pipeline.associated_components:
            if basic_utils.get_file_name(pipeline_key) not in exclude_services:
                if 'ProxyRef' in pipeline.associated_components[pipeline_key]:
                    # if repo not in pipeline_key: #para eliminar los duplicados, pero hay que revisar y testear bien
                    associate_component.append(proxy_services.create_proxy_object(repo, path, f'{basic_utils.get_last_part_value_from_character('/', pipeline_key)}.proxy'))
                    associate_component = self.create_sub_child_service_relations(repo, path, associate_component)
                if 'BusinessServiceRef' in pipeline.associated_components[pipeline_key]:
                    associate_component.append(business_service.create_business_object(repo, path, pipeline.pipeline_name, f'{basic_utils.get_last_part_value_from_character('/', pipeline_key)}.bix'))
        return associate_component
        
    def create_sub_child_service_relations(self, repo, path, associated_child_components):
        pipeline = Pipeline('','')
        for pipeline_child_relation in associated_child_components:
            if isinstance(pipeline_child_relation, ProxyService):
                if pipeline_child_relation.proxy_type != 'external dependency':
                    pipeline_child_relation.pipeline = pipeline.create_pipeline_object(repo, path, pipeline_child_relation, pipeline_child_relation.pipeline_relation)
                    pipeline_child_relation.pipeline = self.create_child_service_relations(repo, path, pipeline_child_relation.pipeline)
        return associated_child_components
        