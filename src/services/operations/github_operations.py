from src.utils import logger_utils
from src.utils import basic_utils
from src.services.api.github_api import GithubApi
import os
from dotenv import load_dotenv 
import logging
from src.services.operations.osb_operations import OsbProject
from src.services.operations.proxy_operations import ProxyServiceLocal
from src.services.operations.pipeline_operations import  PipelineLocal
from src.services.operations.business_operations import BusinessServiceLocal 

# Inicializamos el logger
logger_utils.setup_logging()
logger = logging.getLogger(__name__)

# Inicializamos las variables de entorno
load_dotenv() 

class GithubOperations():
    
    def get_github_repositories(self):
        repositories = []
        github_api = GithubApi(os.getenv("GITHUB_ENDPOINT"))
        github_repositories = github_api.get_all_github_repos()
        github_repositories_list = basic_utils.string_to_json(github_repositories.text)
        services_allowed = basic_utils.create_list_from_properties(os.getenv("SERVICES_START_NAME"))
        for github_repo in github_repositories_list['items']:
            for allowed in services_allowed:
                if github_repo['name'].startswith(allowed):
                    repositories.append(github_repo['name'])
        return repositories

    def create_components_relation(self) -> None:
        
        osb_project = OsbProject('')
        proxy_services = ProxyServiceLocal('','','','')
        pipeline = PipelineLocal('','')
        repository = self.get_github_repositories()
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
