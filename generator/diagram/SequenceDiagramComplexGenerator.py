from graphviz import Digraph
import generator.diagram.SequenceDiagramSimpleGenerator
import utils.DirectoriesOperations
import utils.FilesOperations


def digraph_sequence_osb_complex_generator(service_name):
    consolidate_digraph = Digraph('G', directory=utils.FilesOperations.read_properties('DigraphSection',
                                                                                       'digraph.sequence.path'))
    proxy_list = []
    pipeline_list = []
    business_list = []
    operation_list = []
    proxy_second_list = []
    pipeline_second_list = []
    business_second_list = []
    operation_second_list = []
    resources_list = []
    found_dir = False
    service_object = utils.DirectoriesOperations.navigate_path(service_name)
    service_object = [x for x in service_object if x is not False if x is not True]
    for list_name in service_object:
        for name in list_name:
            if ".proxy" in name:
                proxy_list.append(name)
            if ".pipeline" in name:
                pipeline_list.append(name)
            if ".bix" in name:
                business_list.append(name)
            if not name.endswith(('.proxy', '.pipeline', '.bix')):
                operation_list.append(name)
            if "DS" in name and ".bix" in name:
                if "Business" or "Bussines" in name:
                    name = name.split("Business", 1)[0]
                    name = name.split("DS", 1)[0]
                    name = "Cibt-OSB-" + name + "-DS"
                    service_second_object = utils.DirectoriesOperations.navigate_path(name)
                    if [x for x in service_second_object if x is True]:
                        found_dir = True
                    service_second_object = [x for x in service_second_object if x is not False if x is not True]
                    for list_second_name in service_second_object:
                        for second_name in list_second_name:
                            if ".proxy" in second_name:
                                proxy_second_list.append(second_name)
                            if ".pipeline" in second_name:
                                pipeline_second_list.append(second_name)
                            if ".bix" in second_name:
                                business_second_list.append(second_name)
                            if type(second_name) == list:
                                for second_resources in second_name:
                                    if ".jca" in second_resources:
                                        resources_list.append(second_name)
                            if type(second_name) != list:
                                if not second_name.endswith(('.proxy', '.pipeline', '.bix', '.jca')):
                                    operation_second_list.append(second_name)
                ds_digraph = generator.diagram.SequenceDiagramSimpleGenerator.uml_ds_generator(proxy_second_list,
                                                                                               pipeline_second_list,
                                                                                               business_second_list,
                                                                                               operation_second_list,
                                                                                               resources_list,
                                                                                               found_dir)
            if "CS" in name and ".bix" in name:
                if "Business" in name:
                    name = name.split("Business", 1)[0]
                    name = name.split("CS", 1)[0]
                    name = "Cibt-OSB-" + name + "-CS"
                    service_second_object = utils.DirectoriesOperations.navigate_path(name)
                    if [x for x in service_second_object if x is True]:
                        found_dir = True
                    service_second_object = [x for x in service_second_object if x is not False if x is not True]
                    for list_second_name in service_second_object:
                        for second_name in list_second_name:
                            if ".proxy" in second_name:
                                proxy_second_list.append(second_name)
                            if ".pipeline" in second_name:
                                pipeline_second_list.append(second_name)
                            if ".bix" in second_name:
                                business_second_list.append(second_name)
                            if type(second_name) == list:
                                for second_resources in second_name:
                                    if ".jca" in second_resources:
                                        resources_list.append(second_name)
                            if type(second_name) != list:
                                if not second_name.endswith(('.proxy', '.pipeline', '.bix', '.jca')):
                                    operation_second_list.append(second_name)
                    ds_digraph = generator.diagram.SequenceDiagramSimpleGenerator.uml_cs_generator(proxy_second_list,
                                                                                                   pipeline_second_list,
                                                                                                   business_second_list,
                                                                                                   operation_second_list,
                                                                                                   resources_list,
                                                                                                   found_dir)
    vs_digraph = generator.diagram.SequenceDiagramSimpleGenerator.uml_vs_generator(proxy_list, pipeline_list,
                                                                                   business_list, operation_list,
                                                                                   found_dir)
    consolidate_file = utils.FilesOperations.consolidate_digraph(str(vs_digraph), str(ds_digraph))

    for line_consolidated in consolidate_file:
        consolidate_digraph.body.append(line_consolidated)
    consolidate_digraph.view(filename=service_name,  quiet=False)


def digraph_sequence_soa_complex_generator(service_name):
    consolidate_digraph = Digraph('G', directory=utils.FilesOperations.read_properties('DigraphSection',
                                                                                       'digraph.sequence.path'),
                                  strict=True)
    consolidate_digraph.attr(pad="0.5", nodesep="1", ranksep="1.8")
    proxy_list = []
    pipeline_list = []
    business_list = []
    operation_list = []
    service_list = []
    bpel_list = []
    mediator_list = []
    references_list = []
    bbdd_list = []
    found_dir = False
    service_object = utils.DirectoriesOperations.navigate_path(service_name)
    service_object = [x for x in service_object if x is not False if x is not True]
    for list_name in service_object:
        for name in list_name:
            if ".proxy" in name:
                proxy_list.append(name)
            if ".pipeline" in name:
                pipeline_list.append(name)
            if ".bix" in name:
                replace_name = name
                replace_name = replace_name.replace(".bix", "")
                replace_name = replace_name.replace("Business", "")
                business_list.append(replace_name)
            if not name.endswith(('.proxy', '.pipeline', '.bix')):
                operation_list.append(name)
            if "BAS" in name and ".bix" in name:
                if "Business" in name:
                    name = name.split("Business", 1)[0]
                    name = name.split("BAS", 1)[0]
                    name = "Cibt-SOA-" + name + "-BAS"
                else:
                    name = name.split("BAS", 1)[0]
                    name = name.replace("BAS", "")
                    name = "Cibt-SOA-" + name + "-BAS"
                service_second_object = utils.DirectoriesOperations.navigate_path(name)
                if [x for x in service_second_object if x is True]:
                    found_dir = True
                service_second_object = [x for x in service_second_object if x is not False if x is not True]
                for list_second_name in service_second_object:
                    for second_name in list_second_name:
                        if utils.FilesOperations.read_properties('ProjectExtension',
                                                                 'projectextension.soa.bpel') in second_name:
                            print("BPEL")
                            bpel_list.append(second_name)
                        if utils.FilesOperations.read_properties('ProjectExtension',
                                                                 'projectextension.soa.mediator') in second_name:
                            print("Mediator")
                            mediator_list.append(second_name)
                        if type(second_name) != list:
                            if not second_name.endswith(('.mplan', '.bpel')):
                                service_list.append(second_name)

                        if type(second_name) == list:
                            references_list.append(second_name)

                soa_digraph = generator.diagram.SequenceDiagramSimpleGenerator.uml_bpel_generator(business_list,
                                                                                                  mediator_list,
                                                                                                  bpel_list,
                                                                                                  references_list)

    vs_digraph = generator.diagram.SequenceDiagramSimpleGenerator.uml_vs_generator(proxy_list, pipeline_list,
                                                                                   business_list, operation_list,
                                                                                   found_dir)
    consolidate_file = utils.FilesOperations.consolidate_digraph(str(vs_digraph), str(soa_digraph))

    for line_consolidated in consolidate_file:
        consolidate_digraph.body.append(line_consolidated)
    consolidate_digraph.view(filename=service_name,  quiet=False)


if __name__ == "__main__":
    # digraph_sequence_soa_complex_generator("Cibt-OSB-ManageCountry-VS")
    digraph_sequence_osb_complex_generator("Cibt-OSB-Organisation-VS")
    # digraph_sequence_soa_complex_generator("Cibt-OSB-ManageSalesCase-VS")
    # digraph_sequence_soa_complex_generator("Cibt-OSB-ManageProductType-VS")
    # digraph_sequence_soa_complex_generator("Cibt-OSB-ManagePolicy-VS")
