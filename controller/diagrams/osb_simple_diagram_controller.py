from os import path
from utils.logger_config import LoggerConfig as log_config
import logging
import re
from graphviz import Digraph
from utils import basic_utils
from drawpyo.diagram_types import TreeDiagram, NodeObject

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbSimpleDiagramController:
    def __init__(self, service_files):
        self.service_files = service_files
        
    def create_simple_diagram(self, repo, proxy_components, pipeline_components, business_components): 

        proxy_components_aux={}
        proxy_components_aux.update(proxy_components)
        tree = TreeDiagram(
            file_path = path.join(path.expanduser('~'), "Test Drawpyo Charts"),
            file_name = f'{repo}.drawio',
            direction = "down",
            link_style = "orthogonal",
        )
        
        duplicated_items = self.get_duplicated_components(pipeline_components)
        proxy_components = self.get_principal_proxy_components(duplicated_items, proxy_components)
        
        for proxy in proxy_components:
            proxy_diagram =NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(proxy)), base_style="rounded", fillColor='#dae8fc')
            pipeline_diagram = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(proxy_components[proxy])), parent=proxy_diagram, fillColor='#d5e8d4')
            for pipeline_relations in pipeline_components[proxy_components[proxy]]:
                if basic_utils.get_extension(pipeline_relations) == '.proxy':
                    pipeline_first_relation_diagram = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(pipeline_relations)), parent=pipeline_diagram, fillColor='#dae8fc')
                elif basic_utils.get_extension(pipeline_relations) == '.bix':
                    pipeline_first_relation_diagram = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(pipeline_relations)), parent=pipeline_diagram, fillColor='#ffe6cc')
                if basic_utils.get_extension(pipeline_relations) == '.proxy':
                    if pipeline_relations in proxy_components_aux:
                        pipeline_second_relation_diagram = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(proxy_components_aux[pipeline_relations])), parent=pipeline_first_relation_diagram, fillColor='#d5e8d4')
                        for business_relations in pipeline_components[proxy_components_aux[pipeline_relations]]:
                            business_diagrams = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(business_relations)), parent=pipeline_second_relation_diagram, fillColor='#ffe6cc')
                            # business_endpoint_diagram = NodeObject(tree=tree, value=business_components[business_relations], parent=business_diagrams, fillColor='#e1d5e7')
                            
            tree.auto_layout()
            tree.write()
            del proxy_diagram,  pipeline_diagram
            if 'pipeline_first_relation_diagram' in locals() and 'pipeline_second_relation_diagram' in locals():
                del pipeline_first_relation_diagram, pipeline_second_relation_diagram
    
    def get_duplicated_components(self, pipeline_components):
        duplicated_match = []
        for pipeline in pipeline_components:
            for pipeline_component_list in pipeline_components[pipeline]:
                if pipeline_component_list in pipeline_components[pipeline] and basic_utils.get_extension(pipeline_component_list) == '.proxy':
                    duplicated_match.append(pipeline_component_list) 
            duplicated_match = basic_utils.remove_duplicate_items(duplicated_match)
        return duplicated_match

    def get_principal_proxy_components(self, duplicated_items, proxy_components):
        for i in duplicated_items[:]:
            if i in proxy_components:
                proxy_components.pop(i)
        return proxy_components