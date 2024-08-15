from os import path
import logging
from utils.logger_config import LoggerConfig as log_config
from utils import basic_utils
from drawpyo.diagram_types import TreeDiagram, NodeObject

# Inicializamos el logger
log_config.setup_logging()
logger = logging.getLogger(__name__)

class OsbDiagramService:
        
    def osb_basic_diagram(self, osb_project):
        tree = TreeDiagram(
        file_path = path.join(path.expanduser('~'), "osb-diagrams"),
        file_name = f'{osb_project.project_name}.drawio',
        direction = "down",
        link_style = "orthogonal",
        )
         
        for proxy in osb_project.project:
            proxy_value =NodeObject(tree=tree, value=proxy.proxy_name, base_style="rounded", fillColor='#dae8fc', width = 180)
            pipeline_value = NodeObject(tree=tree, value=proxy.pipeline_relation, parent=proxy_value, fillColor='#d5e8d4', width = 180)
            if len(proxy.pipeline.proxy_service) > 0:
                tree = self.recursive_proxy_childs(tree, proxy, pipeline_value)
            if len(proxy.pipeline.business_service) > 0:
                tree = self.recursive_business_childs(tree, proxy, pipeline_value)
           
        tree.auto_layout()
        tree.write()    
            
    def recursive_proxy_childs(self, recursive_tree, proxy_service, parent_value):
        for proxy_child in proxy_service.pipeline.proxy_service:
            proxy_value =NodeObject(tree=recursive_tree, value=proxy_child.proxy_name, base_style="rounded", parent=parent_value, fillColor='#dae8fc', width = 180)       
            pipeline_value = NodeObject(tree=recursive_tree, value=proxy_child.pipeline_relation, parent=proxy_value, fillColor='#d5e8d4', width = 180)
            if len(proxy_child.pipeline.proxy_service) > 0:
                recursive_tree = self.recursive_proxy_childs(recursive_tree, proxy_child, pipeline_value)
            if len(proxy_child.pipeline.business_service) > 0:
                recursive_tree = self.recursive_business_childs(recursive_tree, proxy_child, pipeline_value)
        return recursive_tree
    
    def recursive_business_childs(self, recursive_tree, proxy_service, parent_value):
        for proxy_child in proxy_service.pipeline.business_service:
            NodeObject(tree=recursive_tree, value=proxy_child.business_name, base_style="rounded", parent=parent_value, fillColor='#ffe6cc', width = 180)       
        return recursive_tree
            
            
    def osb_http_diagram(self, repo, proxy_components, pipeline_components, business_components): 
        proxy_components_aux={}
        proxy_components_aux.update(proxy_components)
        pipeline_components_aux = {}
        external_jms_dependency = {}
        last_child = ''
        check_proxy_diagrams = []
        tree = TreeDiagram(
            file_path = path.join(path.expanduser('~'), "osb-diagrams"),
            file_name = f'{repo}.drawio',
            direction = "down",
            link_style = "orthogonal",
        )
        
        duplicated_items = self.get_duplicated_components(pipeline_components)
        proxy_components = self.get_principal_proxy_components(duplicated_items, proxy_components)
        
        for proxy in proxy_components:
            proxy_diagram =NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(proxy)), base_style="rounded", fillColor='#dae8fc', width = 180)
            pipeline_diagram = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(proxy_components[proxy])), parent=proxy_diagram, fillColor='#d5e8d4', width = 180)
            if proxy_components[proxy] in pipeline_components:
                for pipeline_relations in pipeline_components[proxy_components[proxy]]:
                    if basic_utils.get_last_part_value_from_character('.', pipeline_relations) == 'proxy':
                        if type(pipeline_relations) is not list:
                                    child_pipeline_relations_list = []
                                    child_pipeline_relations_list.append(pipeline_relations)
                        else:
                            child_pipeline_relations_list = pipeline_relations
                        tree = self.write_recursive_child(tree, child_pipeline_relations_list,pipeline_diagram, proxy_components_aux, pipeline_components, pipeline_components_aux, last_child, check_proxy_diagrams, external_jms_dependency)
                    elif basic_utils.get_last_part_value_from_character('.', pipeline_relations) == 'bix':
                        business_diagram = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(pipeline_relations)), parent=pipeline_diagram, fillColor='#ffe6cc', width = 180) 
            tree.auto_layout()
            tree.write()
                
                               
    def osb_jms_diagram(self, repo, proxy_components, pipeline_components, business_components, proxy_jms_types, pipeline_jms_types):
        proxy_components_aux={}
        pipeline_jms_list = []
        external_jms_dependency = {}
        pipeline_components_jms = {}
        last_child = ''
        check_proxy_diagrams = []
        proxy_components_aux.update(proxy_components)
        tree = TreeDiagram(
            file_path = path.join(path.expanduser('~'), "osb-diagrams"),
            file_name = f'{repo}.drawio',
            direction = "down",
            link_style = "orthogonal",
            
        )
      
        for proxy_jms in pipeline_jms_types:
            cont = 0
            while cont < len(pipeline_jms_types[proxy_jms]):
                if "proxy" not in pipeline_jms_types[proxy_jms][cont] and "pipeline" not in pipeline_jms_types[proxy_jms][cont] and "bix" not in pipeline_jms_types[proxy_jms][cont]:
                    try:
                        proxy_jms_key = list(proxy_jms_types.keys())[list(proxy_jms_types.values()).index(pipeline_jms_types[proxy_jms][cont])]
                        pipeline_jms_list.append(proxy_jms_key)
                    except:
                        logger.info('Found external dependency')
                        external_jms_dependency[proxy_jms] = pipeline_jms_types[proxy_jms][cont]
                cont = cont+1
            pipeline_components_jms[proxy_jms] = pipeline_jms_list
            pipeline_jms_list = []
        
        for duplicated_proxies in pipeline_components_jms.values():
            for duplicate_proxy in duplicated_proxies:
                if duplicate_proxy in proxy_components_aux and duplicate_proxy in proxy_components:
                    proxy_components.pop(duplicate_proxy)
               
        for proxy in proxy_components:
            check_external_jms_dependency = False
            proxy_diagram =NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(proxy)), base_style="rounded", fillColor='#dae8fc', width = 180)
            pipeline_diagram = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(proxy_components_aux[proxy])), parent=proxy_diagram, fillColor='#d5e8d4', width = 180)
            if proxy_components_aux[proxy] in pipeline_components_jms and len(pipeline_components_jms[proxy_components_aux[proxy]]) > 0:
                for pipeline_relations in pipeline_components_jms[proxy_components_aux[proxy]]:
                    if basic_utils.get_last_part_value_from_character('.', pipeline_relations) == 'proxy':
                        if type(pipeline_relations) is not list:
                                    child_pipeline_relations_list = []
                                    child_pipeline_relations_list.append(pipeline_relations)
                        else:
                            child_pipeline_relations_list = pipeline_relations
                        tree = self.write_recursive_child(tree, child_pipeline_relations_list,pipeline_diagram, proxy_components_aux, pipeline_components, pipeline_components_jms, last_child, check_proxy_diagrams, external_jms_dependency)
                    elif basic_utils.get_last_part_value_from_character('.', pipeline_relations) == 'bix':
                        logger.debug('Aqui pintaremos los business services')
                        business_diagram_child = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(pipeline_relations)), parent=proxy_diagram, fillColor='#d5e8d4', width = 180)
            elif proxy_components_aux[proxy] in pipeline_components.keys():
                for business_parent_values in pipeline_components[proxy_components_aux[proxy]]:
                    object_color = basic_utils.get_node_color(business_parent_values)
                    business_diagram = NodeObject(tree=tree, value=basic_utils.delete_extension(basic_utils.get_file_name(business_parent_values)), parent=pipeline_diagram, fillColor=object_color, width = 180)     
                    try: 
                        if proxy_components[proxy] in external_jms_dependency.keys() and check_external_jms_dependency == False:
                            business_value = NodeObject(tree=tree, value=f'external dependency\nJMS Type {external_jms_dependency[proxy_components[proxy]]}',parent=pipeline_diagram, fillColor='#e1d5e7', width = 180)
                            check_external_jms_dependency = True
                    except:
                        logger.info(f'we find error but we follow the flow.\n proxy -->{proxy}')
        tree.auto_layout()
        tree.write()

    
    def write_recursive_child(self, recursive_tree, child_proxies,parent_value, pipeline_values, business_values, proxy_child_relations,last_proxy, check_proxy_painted, external_dependency):
        check_external_dependency = False
        check_proxy_diagrams = check_proxy_painted
        for child_proxy in child_proxies:
            if last_proxy is not child_proxy:
                proxy_value = NodeObject(tree=recursive_tree, value=basic_utils.delete_extension(basic_utils.get_file_name(child_proxy)), parent=parent_value, fillColor='#dae8fc', width = 180)
                if child_proxy in pipeline_values:
                    pipeline_value = NodeObject(tree=recursive_tree, value=basic_utils.delete_extension(basic_utils.get_file_name(pipeline_values[child_proxy])),   parent=proxy_value, fillColor='#d5e8d4', width = 180)
                    if pipeline_values[child_proxy] in proxy_child_relations.keys():
                        check_proxy_diagrams.append(child_proxy)
                        if len(proxy_child_relations[pipeline_values[child_proxy]]) > 0:
                            recursive_tree = self.write_recursive_child(recursive_tree, proxy_child_relations[pipeline_values[child_proxy]], pipeline_value,pipeline_values,business_values, proxy_child_relations, child_proxy, check_proxy_diagrams, external_dependency)
                    if pipeline_values[child_proxy] in business_values.keys():
                        for external_calls in business_values[pipeline_values[child_proxy]]:
                            if external_calls not in check_proxy_painted and external_calls in pipeline_values.keys():
                                if type(external_calls) is not list:
                                    child_business_relations_list = []
                                    child_business_relations_list.append(external_calls)
                                else:
                                    child_business_relations_list = external_calls
                                recursive_tree = self.write_recursive_child(recursive_tree, child_business_relations_list, pipeline_value,pipeline_values,business_values, proxy_child_relations, child_proxy, check_proxy_diagrams, external_dependency)
                            object_color = basic_utils.get_node_color(external_calls)
                            try: 
                                if external_calls not in proxy_child_relations[pipeline_values[child_proxy]]:
                                    if pipeline_values[external_calls] not in  proxy_child_relations.keys() and external_calls not in child_business_relations_list:
                                        business_value = NodeObject(tree=recursive_tree, value=basic_utils.delete_extension(basic_utils.get_file_name(external_calls)),parent=pipeline_value, fillColor=object_color, width = 180)
                                    if pipeline_values[child_proxy] in external_dependency.keys() and check_external_dependency == False:
                                        business_value = NodeObject(tree=recursive_tree, value=f'external dependency\nJMS Type {external_dependency[pipeline_values[child_proxy]]}',parent=pipeline_value, fillColor='#e1d5e7', width = 180)
                                        check_external_dependency = True
                            except:
                                business_value = NodeObject(tree=recursive_tree, value=basic_utils.delete_extension(basic_utils.get_file_name(external_calls)),parent=pipeline_value, fillColor=object_color, width = 180)
        return recursive_tree
    
    def get_duplicated_components(self, pipeline_components):
        duplicated_match = []
        for pipeline in pipeline_components:
            for pipeline_component_list in pipeline_components[pipeline]:
                if pipeline_component_list in pipeline_components[pipeline] and basic_utils.get_last_part_value_from_character('.',pipeline_component_list) == 'proxy':
                    duplicated_match.append(pipeline_component_list) 
            duplicated_match = basic_utils.remove_duplicate_items(duplicated_match)
        return duplicated_match

    def get_principal_proxy_components(self, duplicated_items, proxy_components):
        for i in duplicated_items[:]:
            if i in proxy_components:
                proxy_components.pop(i)
        return proxy_components
