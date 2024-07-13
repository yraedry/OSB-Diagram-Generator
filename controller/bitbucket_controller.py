import os
from utils.properties_operations import PropertyOperations as property_config
from utils.logger_config import LoggerConfig as log_config
from utils import basic_utils
from controller.api.bitbucket import BitBucketApi
from controller.diagrams.osb_simple_diagram_controller import OsbSimpleDiagramController
import logging
import xml.etree.ElementTree as ET

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class BitBucketController:
    def __init__(self):
        self.repos = ""
       
    def get_bitbucket_repos(self):
        # Metodo para obtener los repositorios que elijamos por parametro y poder listarlos en un dropdownlist
        services_repo=[]
        services_allowed = basic_utils.create_list_from_properties(property_config.read_properties('ServicesSection', 'services.start.name'))
        request_bitbucket = BitBucketApi(property_config.read_properties('GithubSection', 'github.endpoint'))
        response_api = request_bitbucket.call_bitbucket_api(f'?limit={property_config.read_properties('GithubSection', 'github.param')}')
        
        for line in response_api['values']:
            if len(services_allowed) > 0 and services_allowed[0] != '': 
                for allowed in services_allowed:
                    if allowed in line['name']:
                        services_repo.append(line['name'])
            else:
                services_repo.append(line['name'])
        return services_repo
        
    def get_services_files(self, repo):
        service_files_repo=[]
        request_bitbucket = BitBucketApi(property_config.read_properties('GithubSection', 'github.endpoint'))
        response_api = request_bitbucket.call_bitbucket_api(f'/{repo}/files?limit=999999')
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
        last_match = ''
        match = ''
        request_bitbucket = BitBucketApi(property_config.read_properties('GithubSection', 'github.endpoint'))
        proxy_relations = self.get_proxy_relations(request_bitbucket, repo, components)
        proxy_components.update(proxy_relations)
        for proxy_value in proxy_components:
            pipeline_match = basic_utils.get_file_name(proxy_components[proxy_value])
            if (last_match != ''):                     
                match = pipeline_match
            else:
                last_match = pipeline_match
            pipeline_relations = (self.get_pipelines_relations(request_bitbucket, repo, proxy_components[proxy_value], match, last_match))
            pipeline_components.update(pipeline_relations)
            for business_name in pipeline_components[proxy_components[proxy_value]]:
                business_relations = (self.get_business_relations(request_bitbucket, repo, business_name))
                if business_relations is not None and len(business_relations) > 0:
                    business_components.update(business_relations)
                logger.debug(business_name)        
        service_components.append(proxy_components)
        osb_simple_diagram = OsbSimpleDiagramController(service_components)
        osb_simple_diagram.create_simple_diagram(repo, proxy_components, pipeline_components, business_components)
        
    def get_proxy_relations(self, request_bitbucket, repo, components):
        proxy_components_relations={}
        for component in components:
            response_api = request_bitbucket.call_bitbucket_api(f'/{repo}/browse/{component}?limit=999999')
            response_to_xml = basic_utils.response_json_to_xml(response_api)
            response_xml = ET.fromstring(response_to_xml).find(".//{http://www.bea.com/wli/sb/services}invoke")
            pipeline_path_name = response_xml.attrib['ref']
            proxy_components_relations[component] = f'{pipeline_path_name}.pipeline'
            logger.debug(pipeline_path_name)
            # data = readfromstring(my_json)
            # xml_data = json2xml.Json2xml(data).to_xml()
            # for line in response_api['lines']:
            #     if 'invoke' in line['text']:
            #         pattern = r'ref="(.*?)"'
            #         pipeline_match = basic_utils.get_string_from_pattern(pattern, line['text'])
            #         proxy_components_relations[component] = f'{pipeline_match}.pipeline'
        return proxy_components_relations
    
    def get_pipelines_relations(self, request_bitbucket, repo, pipeline_name, match, last_match):
        pipeline_relations_list =[]
        exclude_services= basic_utils.create_list_from_properties(property_config.read_properties('ExcludeSection', 'exclude.proxies'))
        pipeline_components_relations={}
        response_api = request_bitbucket.call_bitbucket_api(f'/{repo}/browse/{pipeline_name}?limit=999999')
        for line in response_api['lines']:
            if 'BusinessServiceRef' in line['text'] or 'ProxyRef' in line['text']:
                pattern = r'ref="(.*?)"'
                business_match = basic_utils.get_string_from_pattern(pattern, line['text'])
                if match != last_match and basic_utils.get_file_name(business_match) not in exclude_services:
                    if last_match != '' and match =='' and 'BusinessServiceRef' in line['text']:
                        pipeline_relations_list.append(f'{business_match}.bix')
                    elif last_match != '' and match !='' and 'BusinessServiceRef' in line['text']:
                        pipeline_relations_list.append(f'{business_match}.bix')
                    elif last_match != '' and match =='' and 'ProxyRef' in line['text']:
                        pipeline_relations_list.append(f'{business_match}.proxy')
                    elif last_match != '' and match !='' and 'ProxyRef' in line['text']:
                        pipeline_relations_list.append(f'{business_match}.proxy')
                pipeline_relations_list = basic_utils.remove_duplicate_items(pipeline_relations_list)
                pipeline_components_relations[pipeline_name] = pipeline_relations_list
        return pipeline_components_relations

    def get_business_relations(self, request_bitbucket, repo, business_name):
        business_components_relations={}
        response_api = request_bitbucket.call_bitbucket_api(f'/{repo}/browse/{business_name}?limit=999999')
        if('errors' not in response_api):
            for line in response_api['lines']:
                if 'value' in line['text']:     
                    pattern = r'value>(.*?)</'
                    endpoint = basic_utils.get_string_from_pattern(pattern, line['text'])
                    business_components_relations[business_name] = endpoint
        return business_components_relations

    def create_file_bitbucket_repos(self) -> None:
        # Metodo para obtener los repositorios que elijamos por parametro y guardarlos en un fichero
        request_bitbucket = BitBucketApi(property_config.read_properties('GithubSection', 'github.endpoint'))
        services_allowed = basic_utils.create_list_from_properties(property_config.read_properties('ServicesSection', 'services.start.name'))
        response_api = request_bitbucket.call_bitbucket_api(f'?limit={property_config.read_properties('GithubSection', 'github.param')}')
        service_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir + "/properties")
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
        request_bitbucket = BitBucketApi(property_config.read_properties('GithubSection', 'github.endpoint')) 
        get_repo = request_bitbucket.call_bitbucket_api(f'/{repos}/files')
        for component in get_repo['values']:
            extension = os.path.splitext(component)
            if extension[1] == ('.bix') or extension[1] == '.proxy' or extension[1] == '.pipeline':
                components_repo.append(component) 
