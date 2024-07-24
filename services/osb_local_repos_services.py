import os
from utils.properties_operations import PropertyOperations as property_config
from utils import basic_utils, xml_utils
from utils.logger_config import LoggerConfig as log_config
from services.osb_diagram_services import OsbDiagramService
from controller.files_controller import FilesController
import logging

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbLocalReposService:
    def __init__(self, path):
        self.path = path

    def get_services_files(self) -> None:
        service_files_repo=[]
        file_controller = FilesController(self.path)
        service_files_repo = file_controller.get_repositories_path()
        self.get_components_relations(service_files_repo)


    def get_components_relations(self, components) -> None:
        service_components=[]
        proxy_relations = []
        pipeline_relations =[]
        business_relations =[]
        proxy_components={}
        pipeline_components={}
        business_components={}
        pipeline_jms_type_relations={}
        proxy_jms_type_relations={}
        proxies_type = {}
        repository = self.get_repository_name(components)
        proxy_relations = self.get_proxy_relations(repository)
        proxy_components.update(proxy_relations)
        proxies_type = self.get_jms_type_proxy(repository)
        
        for proxy_value in proxy_components:
            if len(proxy_jms_type_relations) == 0:
                proxy_jms_type_relations = self.get_jms_type_proxy(repository)
            else:
                proxy_jms_type_relations.update(self.get_jms_type_proxy(repository))
        #     pipeline_relations = (self.get_pipelines_relations(repository))
        #     if len(pipeline_jms_type_relations) == 0:
        #         pipeline_jms_type_relations = self.get_jms_type_pipeline(repository, len(proxies_type))
        #     else:
        #         pipeline_jms_type_relations.update(self.get_jms_type_pipeline(repository, len(proxies_type)))
        #     if len(pipeline_relations) > 0:
        #         pipeline_components.update(pipeline_relations)
        # logger.debug(proxies_type)
        #         for business_name in pipeline_components[proxy_components[proxy_value]]:
        #             business_relations = (self.get_business_relations(repo, business_name))
        #             if business_relations is not None and len(business_relations) > 0:
        #                 business_components.update(business_relations)      
        # service_components.append(proxy_components)
        # osb_diagram = OsbDiagramService()
        # if len(proxy_jms_type_relations) == 0 and len(pipeline_jms_type_relations) == 0:
        #     osb_diagram.osb_http_diagram(repo, proxy_components, pipeline_components, business_components)
        # else:
        #     osb_diagram.osb_jms_diagram(repo, proxy_components, pipeline_components, business_components, proxy_jms_type_relations, pipeline_jms_type_relations)

    def get_proxy_relations(self, repo):
        proxy_components_relations={}
        file_type = 'proxy'
        proxy_content = self.get_xml_values(repo, file_type)
        for xml_values in proxy_content:
            pipeline_path_name = xml_utils.find_proxy_invoke(proxy_content[xml_values])
            proxy_path_name = f'{basic_utils.get_previous_part_value_from_character('/', pipeline_path_name)}{xml_values}'
            proxy_components_relations[proxy_path_name] = pipeline_path_name
        return proxy_components_relations
    
    def get_jms_type_proxy(self, repo):
        jms_type_proxy_dict = {}
        pattern = r'JMSType = '
        file_type = 'proxy'
        proxy_content = self.get_xml_values(repo, file_type)
        for xml_values in proxy_content:
            proxy_type = xml_utils.find_proxy_type(proxy_content[xml_values])
            if proxy_type is not None and 'JMSType' in proxy_type.text:
                jms_type_proxy_dict[xml_values] = basic_utils.delete_with_pattern(pattern, proxy_type.text)
        return jms_type_proxy_dict
    
    def get_pipelines_relations(self, repo):
        pipeline_relations_list =[]
        exclude_services= basic_utils.create_list_from_properties(property_config.read_properties('services', 'exclude'))
        pipeline_components_relations={}
        file_type = 'pipeline'
        pipeline_content = self.get_xml_values(repo, file_type)
        for xml_values in pipeline_content:
            response_xml = xml_utils.find_pipeline_service(pipeline_content[xml_values])
        for service_match in response_xml:
            if basic_utils.get_file_name(service_match) not in exclude_services:
                if 'ProxyRef' in response_xml[service_match]:
                    pipeline_relations_list.append(f'{service_match}.proxy')
                elif 'BusinessServiceRef' in response_xml[service_match]:
                    pipeline_relations_list.append(f'{service_match}.bix')
            pipeline_components_relations[xml_values] = pipeline_relations_list
        return pipeline_components_relations
    
    def get_jms_type_pipeline(self, repo, proxy_type):
        # revisar este metodo, no esta devolviendo las cosas correctamente
        jms_types_dict = {}
        jms_types_list = []
        file_type = 'pipeline'
        pipeline_content = self.get_xml_values(repo, file_type)
        for xml_values in pipeline_content:
            response_xml = xml_utils.find_pipeline_jms_type(pipeline_content[xml_values])
            if len(response_xml) > 0:
                for jms_type in response_xml:
                    jms_types_list.append(jms_type.text)
                jms_types_dict[xml_values] = jms_types_list
            elif proxy_type > 0:
                jms_types_dict = self.get_pipelines_relations(repo)
        return jms_types_dict
    
    def get_xml_values(self, repo, file_type):
        xml_content = {}
        file_controller = FilesController(self.path)
        if file_type == "proxy":
            xml_path = file_controller.get_proxy_path(repo)
        elif file_type == "pipeline":
            xml_path = file_controller.get_pipeline_path(repo)
        xml_name = file_controller.get_file_from_path(xml_path, file_type)
        for content in xml_name:
            xml_content[content] = file_controller.get_content_file_from_path(xml_path, content)
        return xml_content
        
    def get_repository_name(self, components):
        for component in components:
            repo = basic_utils.get_last_part_value_from_character('\\', component)
        return repo