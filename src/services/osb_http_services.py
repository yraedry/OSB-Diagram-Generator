import os
from dotenv import load_dotenv 
from src.utils import basic_utils, xml_utils
from services.api.bitbucket_api import BitBucketApi
from src.utils import logger_utils
from src.services.osb_diagram_services import OsbDiagramService
import logging
import os
from git import Repo

# Inicializamos el logger
logger_utils.setup_logging()
logger = logging.getLogger(__name__)

# Inicializamos las variables de entorno
load_dotenv() 

class OsbHttpService:
    def __init__(self):
        self.repos = ""
       
    def get_repos(self) -> None:
        # Metodo para obtener los repositorios que elijamos por parametro y poder listarlos en un dropdownlist
        services_repo=[]
        services_allowed = basic_utils.create_list_from_properties(os.getenv("SERVICES_START_NAME"))
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
        response_api = request_bitbucket.get_bitbucket_repos()
        for line in response_api['values']:
            if len(services_allowed) > 0 and services_allowed[0] != '': 
                for allowed in services_allowed:
                    if allowed in line['name']:
                        services_repo.append(line['name'])
            else:
                services_repo.append(line['name'])
        self.create_file_bitbucket_repos()
        self.clone_services_local(services_repo)  
        # return services_repo
        
    def get_services_files(self, repo):
        service_files_repo=[]
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
        response_api = request_bitbucket.get_bitbucket_files(repo)
        for line in response_api['values']:
            if line.endswith('.proxy'):
                service_files_repo.append(line)
        self.get_components_relations(repo, service_files_repo)
        logger.debug(response_api)
        return service_files_repo
    
    def get_components_relations(self, repo, components) -> None:
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
        proxy_relations = self.get_proxy_relations(repo, components)
        proxy_components.update(proxy_relations)
        proxies_type = self.get_type_proxies(repo, proxy_components)
        for proxy_value in proxy_components:
            if len(proxy_jms_type_relations) == 0:
                proxy_jms_type_relations = self.get_jms_type_proxy(repo, proxy_value)
            else:
                proxy_jms_type_relations.update(self.get_jms_type_proxy(repo, proxy_value))
            pipeline_relations = (self.get_pipelines_relations(repo, proxy_components[proxy_value]))
            if len(pipeline_jms_type_relations) == 0:
                pipeline_jms_type_relations = self.get_jms_type_pipeline(repo, proxy_components[proxy_value], len(proxies_type))
            else:
                pipeline_jms_type_relations.update(self.get_jms_type_pipeline(repo, proxy_components[proxy_value], len(proxies_type)))
            if len(pipeline_relations) > 0:
                pipeline_components.update(pipeline_relations)
                for business_name in pipeline_components[proxy_components[proxy_value]]:
                    business_relations = (self.get_business_relations(repo, business_name))
                    if business_relations is not None and len(business_relations) > 0:
                        business_components.update(business_relations)      
        service_components.append(proxy_components)
        osb_diagram = OsbDiagramService()
        if len(proxy_jms_type_relations) == 0 and len(pipeline_jms_type_relations) == 0:
            osb_diagram.osb_http_diagram(repo, proxy_components, pipeline_components, business_components)
        else:
            osb_diagram.osb_jms_diagram(repo, proxy_components, pipeline_components, business_components, proxy_jms_type_relations, pipeline_jms_type_relations)
        
    def get_proxy_relations(self, repo, components):
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
        proxy_components_relations={}
        for component in components:
            response_api = request_bitbucket.get_bitbucket_component(repo, component)
            response_to_xml = basic_utils.response_json_to_xml(response_api)
            pipeline_path_name = xml_utils.find_proxy_invoke(response_to_xml)
            proxy_components_relations[component] = f'{pipeline_path_name}'
        return proxy_components_relations
    
    def get_pipelines_relations(self, repo, pipeline_name):
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
        pipeline_relations_list =[]
        exclude_services= basic_utils.create_list_from_properties(os.getenv("SERVICES_EXCLUDED"))
        pipeline_components_relations={}
        response_api = request_bitbucket.get_bitbucket_component(repo, pipeline_name)
        response_to_xml = basic_utils.response_json_to_xml(response_api)
        if response_to_xml != 'not found':
            try:
                if response_api['isLastPage'] is True:
                    response_xml = xml_utils.find_pipeline_service(response_to_xml)
                else:
                    second_api_request = request_bitbucket.get_bitbucket_component(repo, pipeline_name)
                    second_response_to_xml = basic_utils.response_json_to_xml(second_api_request)
                    response_to_xml = f'{response_to_xml}{second_response_to_xml}'
                    response_xml = xml_utils.find_pipeline_service(response_to_xml)
            except:
                logger.error('found error in service, continue with erros')
            for service_match in response_xml:
                if basic_utils.get_file_name(service_match) not in exclude_services:
                    if 'ProxyRef' in response_xml[service_match]:
                        pipeline_relations_list.append(f'{service_match}.proxy')
                    elif 'BusinessServiceRef' in response_xml[service_match]:
                        pipeline_relations_list.append(f'{service_match}.bix')
                pipeline_components_relations[pipeline_name] = pipeline_relations_list
        return pipeline_components_relations

    def get_business_relations(self, repo, business_name):
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
        business_components_relations={}
        response_api = request_bitbucket.get_bitbucket_component(repo, business_name)
        if('errors' not in response_api):
            response_to_xml = basic_utils.response_json_to_xml(response_api)
            endpoint = xml_utils.find_business_values(response_to_xml)
            if endpoint is not None:
                business_components_relations[business_name] = endpoint.text
        return business_components_relations

    def create_file_bitbucket_repos(self) -> None:
        # Metodo para obtener los repositorios que elijamos por parametro y guardarlos en un fichero
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
        services_allowed = basic_utils.create_list_from_properties(os.getenv("SERVICES_START_NAME"))
        response_api = request_bitbucket.get_bitbucket_repos()
        service_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir + "/files")
        with open(service_dir + "/services.txt", 'w') as f:
            for line in response_api['values']:
                if len(services_allowed) > 0 and services_allowed[0] != '': 
                    for allowed in services_allowed:
                        if allowed in line['name']:
                            f.write(f"{line['name']}\n")
                else:
                    f.write(f"{line['name']}\n")
        f.close()

    def browse_bitbucket_repo(self, repos) -> None:
        # Metodo para obtener los ficheros de los repositorios (metodo simple)
        components_repo = []
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT")) 
        get_repo = request_bitbucket.get_bitbucket_repos()
        for component in get_repo['values']:
            extension = os.path.splitext(component)
            if (extension[1] == '.bix') or (extension[1] == '.proxy') or (extension[1] == '.pipeline'):
                components_repo.append(component) 
    
    def get_jms_type_pipeline(self, repo, component, proxy_type):
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
        jms_types_dict = {}
        jms_types_list = []
        response_api = request_bitbucket.get_bitbucket_component(repo, component)
        response_to_xml = basic_utils.response_json_to_xml(response_api)
        if response_to_xml != 'not found':
            response_xml = xml_utils.find_pipeline_jms_type(response_to_xml)
            if len(response_xml) > 0:
                for jms_type in response_xml:
                    jms_types_list.append(jms_type.text)
                jms_types_dict[component] = jms_types_list
            elif proxy_type > 0:
                jms_types_dict = self.get_pipelines_relations(repo, component)
        return jms_types_dict

    def get_type_proxies(self, repo, components):
            request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
            jms_type_proxy_dict = {}
            pattern = r'JMSType = '
            for component in components:
                response_api = request_bitbucket.get_bitbucket_component(repo, component)
                response_to_xml = basic_utils.response_json_to_xml(response_api)
                proxy_type = xml_utils.find_proxy_type(response_to_xml)
                if proxy_type is not None and 'JMSType' in proxy_type.text:
                    jms_type_proxy_dict[component] = basic_utils.delete_with_pattern(pattern, proxy_type.text)      
            return jms_type_proxy_dict    
        
    def get_jms_type_proxy(self, repo, component):
        request_bitbucket = BitBucketApi(os.getenv("BITBUCKET_ENDPOINT"))
        jms_type_proxy_dict = {}
        pattern = r'JMSType = '
        response_api = request_bitbucket.get_bitbucket_component(repo, component)
        response_to_xml = basic_utils.response_json_to_xml(response_api)
        proxy_type = xml_utils.find_proxy_type(response_to_xml)
        if proxy_type is not None and 'JMSType' in proxy_type.text:
            jms_type_proxy_dict[component] = basic_utils.delete_with_pattern(pattern, proxy_type.text)     
        return jms_type_proxy_dict        
    
    def clone_services_local(self, repos) -> None:
            for repo in repos:
                cwd = os.getcwd()
                service_dir = f'{os.path.abspath(os.path.join(cwd, os.pardir))}\\cloned_repositories\\{repo}\\'
                clone_url = f'{os.getenv("BITBUCKET_CLONE")}/{repo}.git'
                try:
                    if not os.path.exists(service_dir):
                        Repo.clone_from(clone_url, service_dir, config=f'https.proxy=https://{os.getenv("HTTPS_PROXY_NAME")}, x-token-auth:{os.getenv("BITBUCKET_TOKEN")}', branch=os.getenv("BITBUCKET_BRANCH"), allow_unsafe_options=True)
                    else:
                        found_repo = Repo(service_dir)
                        found_repo.remotes[0].pull()
                except:
                    logger.error('found error in clone method')
        