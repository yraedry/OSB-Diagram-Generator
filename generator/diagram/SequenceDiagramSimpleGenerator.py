from graphviz import Digraph
import utils.FilesOperations
import utils.DirectoriesOperations
import copy


def uml_vs_generator(componet_proxy_list, componet_pipeline_list, componet_business_list, componet_operation_list,
                     isdir):
    print('clase UML')
    print(componet_business_list)
    print(componet_pipeline_list)
    print(componet_proxy_list)
    print(componet_operation_list)

    g = Digraph('G', directory=utils.FilesOperations.read_properties('DigraphSection', 'digraph.sequence.path'))

    count_proxy = 0
    check_count_proxy = False
    while count_proxy < len(componet_proxy_list) and check_count_proxy is False:
        if check_count_proxy is False:
            for proxy_name in componet_proxy_list:
                if not("Rest" in proxy_name):
                    if check_count_proxy is False:
                        if "Proxy" in proxy_name:
                            proxy_name = proxy_name.split("Proxy", 1)[0]
                        filename = proxy_name
                        g.node('start', shape='Mdiamond')
                        g.edge('start', proxy_name)
                        g.node(proxy_name, shape='rectangle')
                        count_proxy = count_proxy + 1
                        count_business = 0
                        check_count_business = False
                        while count_business < len(componet_business_list):
                            for business_name in componet_business_list:
                                if check_count_business is False:
                                    if "Business" in business_name:
                                        business_name = business_name.split("Business", 1)[0]
                                    if "Business" in business_name:
                                        business_name = business_name.replace("Business", "")
                                    elif "Bussines" in business_name:
                                        business_name = business_name.replace("Bussines", "")
                                    print(business_name)
                                    business_name = business_name.replace(".bix", "")
                                    count_operations = 0
                                    check_count_operations = False
                                    while count_operations < len(componet_operation_list):
                                        for operation_name in componet_operation_list:
                                            if check_count_operations is False:
                                                operation_concat_name = proxy_name + "." + operation_name
                                                g.edge(proxy_name, operation_concat_name, len='1.00')
                                                g.edge(operation_concat_name, business_name, len='1.00')
                                                g.node(business_name, shape='rectangle')
                                                g.node(operation_concat_name, shape='rectangle')
                                                count_operations = count_operations + 1
                                        check_count_operations = True
                                    count_business = count_business + 1
                            check_count_business = True
            # g.view(filename=filename,  quiet=False)
        check_count_proxy = True
    return g


def uml_ds_generator(componet_proxy_list, componet_pipeline_list, componet_business_list, componet_operation_list,
                     component_database_list, isdir):
    print('clase UML')
    print(componet_business_list)
    print(componet_pipeline_list)
    print(componet_proxy_list)
    print(componet_operation_list)
    print(component_database_list)
    g = Digraph('G', directory=utils.FilesOperations.read_properties('DigraphSection', 'digraph.sequence.path'))

    count_proxy = 0
    check_count_proxy = False
    while count_proxy < len(componet_proxy_list) and check_count_proxy is False:
        if check_count_proxy is False:
            for proxy_name in componet_proxy_list:
                if not("Rest" in proxy_name):
                    if check_count_proxy is False:
                        if "Proxy" in proxy_name:
                            proxy_name = proxy_name.split("Proxy", 1)[0]
                        if "Business" in proxy_name:
                            proxy_name = proxy_name.replace("Business", "")
                        elif "Bussines" in proxy_name:
                            proxy_name = proxy_name.replace("Bussines", "")
                        filename = proxy_name
                        g.node('start', shape='Mdiamond')
                        g.edge('start', proxy_name)
                        g.node(proxy_name, shape='rectangle')
                        count_proxy = count_proxy + 1
                        count_business = 0
                        check_count_business = False
                        while count_business < len(componet_business_list):
                            for business_name in componet_business_list:
                                if check_count_business is False:
                                    if "Business" in business_name:
                                        business_name = business_name.split("Business", 1)[0]
                                    elif "Bussiness" in business_name:
                                        business_name = business_name.split("Bussiness", 1)[0]
                                    print(business_name)
                                    if ".bix" in business_name:
                                        business_name = business_name.replace(".bix", "")
                                    business_concat_name = proxy_name + "." + business_name
                                    g.node(business_concat_name, shape='rectangle')
                                    g.edge(proxy_name, business_concat_name, len='1.00')
                                    for db_name in component_database_list:
                                        if business_name in str(db_name):
                                            for i in range(len(db_name) + 1):
                                                if i % 2 == 0:
                                                    bs_aux = i
                                                if i % 2 == 1:
                                                    database_info = str(db_name[i])
                                                    database_info = database_info.replace("['", "")
                                                    database_info = database_info.replace("']", "")
                                                    database_info = database_info.replace("'", "")
                                                    database_info = database_info.replace(",", "\n")
                                                    if business_name in str(db_name[bs_aux]):
                                                        g.node(database_info, shape="cylinder")
                                                        g.edge(business_concat_name, database_info, len='1.00')
                                                        # Comprobar que lo hace adecuadamente
                                                        break
                                        if isdir is False:
                                            break
                                count_business = count_business + 1
                            check_count_business = True
        # g.view(filename=filename,  quiet=False)
    return g


def uml_cs_generator(componet_proxy_list, componet_pipeline_list, componet_business_list, componet_operation_list,
                     component_database_list, isdir):
    print('clase UML')
    print(componet_business_list)
    print(componet_pipeline_list)
    print(componet_proxy_list)
    print(componet_operation_list)
    print(component_database_list)
    g = Digraph('G', directory=utils.FilesOperations.read_properties('DigraphSection', 'digraph.sequence.path'))

    count_proxy = 0
    check_count_proxy = False
    while count_proxy < len(componet_proxy_list) and check_count_proxy is False:
        if check_count_proxy is False:
            for proxy_name in componet_proxy_list:
                if not("Rest" in proxy_name):
                    if check_count_proxy is False:
                        if "Proxy" in proxy_name:
                            proxy_name = proxy_name.split("Proxy", 1)[0]
                        filename = proxy_name
                        g.node('start', shape='Mdiamond')
                        g.edge('start', proxy_name)
                        g.node(proxy_name, shape='rectangle')
                        count_proxy = count_proxy + 1
                        count_business = 0
                        check_count_business = False
                        while count_business < len(componet_business_list):
                            for business_name in componet_business_list:
                                if check_count_business is False:
                                    if "Business" in business_name:
                                        business_name = business_name.split("Business", 1)[0]
                                    elif "Bussiness" in business_name:
                                        business_name = business_name.split("Bussiness", 1)[0]
                                    print(business_name)
                                    business_concat_name = proxy_name + "." + business_name
                                    g.node(business_concat_name, shape='rectangle')
                                    g.edge(proxy_name, business_concat_name, len='1.00')
                                    for db_name in component_database_list:
                                        print(type(db_name))
                                        if business_name in str(db_name):
                                            for i in range(len(db_name) + 1):
                                                if i % 2 == 0:
                                                    bs_aux = i
                                                if i % 2 == 1:
                                                    database_info = str(db_name[i])
                                                    database_info = database_info.replace("['", "")
                                                    database_info = database_info.replace("']", "")
                                                    database_info = database_info.replace("'", "")
                                                    database_info = database_info.replace(",", "\n")
                                                    if business_name in str(db_name[bs_aux]):
                                                        g.node(database_info, shape="cylinder")
                                                        g.edge(business_concat_name, database_info, len='1.00')
                                                        # Comprobar que lo hace adecuadamente
                                                        break
                                        if isdir is False:
                                            break
                                count_business = count_business + 1
                            check_count_business = True
        # g.view(filename=filename,  quiet=False)
    return g


def uml_bpel_generator(component_service_list, component_mediator_list, component_bpels_list, component_reference_list):
    print('clase UML')
    print(component_service_list)
    print(component_mediator_list)
    print(component_bpels_list)
    print(component_reference_list)
    g = Digraph('G', directory=utils.FilesOperations.read_properties('DigraphSection', 'digraph.sequence.path'),
                strict=True)
    g.attr(pad="0.5", nodesep="1", ranksep="1.8")
    count_service = 0
    check_count_proxy = False
    while count_service < len(component_service_list) and check_count_proxy is False:
        if check_count_proxy is False:
            for service_name in component_service_list:
                if check_count_proxy is False:
                    filename = service_name
                    g.node('start', shape='Mdiamond')
                    g.edge('start', service_name)
                    if "SOA" in service_name:
                        service_name = service_name.split("SOA", 1)[1]
                        service_name = service_name.replace("-", "")
                    g.node(service_name, shape='rectangle')
                    count_service = count_service + 1
                    count_mediator = 0
                    check_count_mediator = False
                    for mediator_name in component_mediator_list:
                        if check_count_mediator is False:
                            if '.mplan' in mediator_name:
                                mediator_name = mediator_name.split(".mplan", 1)[0]
                            g.edge(service_name, mediator_name)
                            g.node(mediator_name, shape='rectangle')
                            count_mediator = count_mediator + 1
                        count_bpel = 0
                        check_count_bpel = False
                        while count_bpel < len(component_bpels_list):
                            for bpel_name in component_bpels_list:
                                if check_count_bpel is False:
                                    if '.bpel' in bpel_name:
                                        bpel_name = bpel_name.split(".bpel", 1)[0]
                                    g.edge(mediator_name, bpel_name)
                                    g.node(bpel_name, shape='rectangle')
                                count_service = 0
                                check_count_service = False
                                print(len(component_reference_list))
                                database_list = []
                                for service_name_list in component_reference_list:
                                    service_name_list_aux = copy.deepcopy(service_name_list)
                                    if check_count_service is False:
                                        for i in range(len(service_name_list)):
                                            if i % 2 == 0:
                                                bs_aux = i
                                                service_concat_name = bpel_name + "." + service_name_list[bs_aux]
                                                print(service_concat_name)
                                                g.node(service_concat_name, shape="cylinder")
                                                g.edge(bpel_name, service_concat_name, len='1.00')
                                                database_list.append(service_name_list[bs_aux])
                                            if i % 2 == 1:
                                                reference_concat_name = service_name_list[bs_aux] + "." + service_name_list[i]
                                                g.node(reference_concat_name, shape="cylinder")
                                                g.edge(service_concat_name, reference_concat_name, len='1.00')
                                                database_list.append(service_name_list[i])
                                                database_object = utils.DirectoriesOperations.iterate_osb_dirs(
                                                    utils.FilesOperations.read_properties('OsbSection', 'osb.path') +
                                                    "Cibt-OSB-" + service_name_list[bs_aux].replace("DS", "")
                                                    .replace("DSRef", "").replace("Ref", "") + "-DS")
                                                check_loop = True
                                                for db_list in database_object[4]:
                                                    if check_loop is True:
                                                        if service_name_list[i] in str(db_list[0]):
                                                            for x in range(len(db_list) + 1):
                                                                if x % 2 == 0:
                                                                    second_count = x
                                                                if x % 2 == 1:
                                                                    database_info = str(db_list[x])
                                                                    database_info = database_info.replace("['", "")
                                                                    database_info = database_info.replace("']", "")
                                                                    database_info = database_info.replace("'", "")
                                                                    database_info = database_info.replace(",", "\n")
                                                                    for pl_name_service in service_name_list_aux:
                                                                        if pl_name_service in str(db_list[second_count]):
                                                                            g.node(database_info, shape="cylinder")
                                                                            g.edge(reference_concat_name, database_info,
                                                                                   len='1.00')
                                                                            # Comprobar que lo hace adecuadamente
                                                                            check_loop = False
                                                                            # del service_name_list_aux[0:2]
                                                                            break
                                    del component_reference_list[0]
                                    count_bpel = count_bpel + 1
                                    break
                            check_count_mediator = True
                            check_count_proxy = True
    # g.view(filename=filename, quiet=False)
    return g
    # g.view(filename=filename,  quiet=False)
