import os
import generator.diagram.SequenceDiagramSimpleGenerator
import utils.FilesOperations


def navigate_path(service_name):
    os.chdir(utils.FilesOperations.read_properties('ExplorerSection', 'Explorer.path') + service_name)
    for x in os.listdir('.'):
        # Hago un split por falta de homogeneidad y en las carpetas
        split_name = service_name.split("-")[2]
        print("------------------------>" + split_name)
        split_type = service_name.split("-")[3]
        service_directory = split_name + split_type

        if os.path.isdir(x) and x in service_directory:
            if 'BAS' in x:
                os.chdir(x + '/SOA')
                path = os.getcwd()
                service_object = iterate_soa_dirs(path)
            else:
                os.chdir(x)
                path = os.getcwd()
                service_object = iterate_osb_dirs(path)
        elif os.path.isdir(x) and x in service_name:
            if 'BAS' in x:
                os.chdir(x + '/SOA')
                path = os.getcwd()
                service_object = iterate_soa_dirs(path)
            else:
                os.chdir(x)
                path = os.getcwd()
                service_object = iterate_osb_dirs(path)
        elif os.path.isdir(x) and split_name in x:
            if 'BAS' in x:
                os.chdir(x + '/SOA')
                path = os.getcwd()
                service_object = iterate_soa_dirs(path)
            else:
                os.chdir(x)
                path = os.getcwd()
                service_object = iterate_osb_dirs(path)
    return service_object


def iterate_osb_dirs(path):
    business_list = []
    proxy_list = []
    pipeline_list = []
    resources_list = []
    operations_list = []
    database_list = []
    count_resources = 0
    first = True
    resources = False
    dir = False
    for contexto, child_dir, child_files in os.walk(path):
        # Borramos las carpetas autogeneradas
        if '.data' in child_dir:
            child_dir.remove('.data')
        elif '.settings' in child_dir:
            child_dir.remove('.settings')
        elif '.git' in child_dir:
            child_dir.remove('.git')
        elif 'System' in child_dir:
            child_dir.remove('System')
        elif 'src' in child_dir:
            child_dir.remove('src')
        elif '.adf' in child_dir:
            child_dir.remove('.adf')
        if utils.FilesOperations.read_properties('ExplorerSection', 'Explorer.business.path') in contexto and \
                resources is False:
            print("Business")
            count = 0
            while count < len(child_files):
                business_list.append(child_files[count])
                count = count + 1
        if utils.FilesOperations.read_properties('ExplorerSection', 'Explorer.proxy.path') in contexto:
            print('Proxy')
            count = 0
            while count < len(child_files):
                proxy_list.append(child_files[count])
                count = count+1
        if utils.FilesOperations.read_properties('ExplorerSection', 'Explorer.pipeline.path') in contexto:
            print('Pipelines')
            os.chdir(contexto)
            print(contexto)
            count = 0
            while count < len(child_files):
                pipeline_list.append(child_files[count])
                operations_list = utils.FilesOperations.match_in_files(contexto, pipeline_list[count])
                count = count + 1
        if utils.FilesOperations.read_properties('ExplorerSection', 'Explorer.Resources.path') in contexto:
            resources = True
            print('Resources')
            os.chdir(contexto)
            print(contexto)
            count = 0
            if len(child_dir) == 0 and first is True:
                count_resources = 0
                first = False
            elif len(child_dir) > 0 and first is True:
                dir = True
                first = False
            resources_list_aux = []
            while count < len(child_files):
                if '.jca' in child_files[count]:
                    resources_list.append(child_files[count])
                    # print(child_files[count_resources])
                    if os.path.isdir(contexto) > 0:
                        resources_list_aux.append(resources_list[count_resources])
                        resources_list_aux.append(utils.FilesOperations.match_in_files(contexto,
                                                                                       resources_list[count_resources]))
                        count_resources = count_resources + 1
                    database_list.append(resources_list_aux)
                count = count + 1
    return proxy_list, pipeline_list, business_list, operations_list, database_list, dir
    # call_generator(proxy_list, pipeline_list, business_list, operations_list, database_list, dir)


def iterate_soa_dirs(path):
    service_list = []
    mediator_list = []
    bpels_list = []
    operation_list = []
    database_list = []
    for contexto, child_dir, child_files in os.walk(path):
        if 'SCA-INF' in child_dir:
            child_dir.remove('SCA-INF')
        if '.designer' in child_dir:
            child_dir.remove('.designer')
        if utils.FilesOperations.read_properties('ExplorerSection', 'Explorer.bpel.path') in contexto:
            print("BPEL")
            count = 0
            while count < len(child_files):
                bpels_list.append(child_files[count])
                # operation_list = (utils.FilesOperations.match_in_files(contexto, child_files[count]))
                operation_list.append(utils.FilesOperations.search_bpel_references(contexto, child_files[count]))
                count = count + 1
        if utils.FilesOperations.read_properties('ExplorerSection', 'Explorer.mediator.path') in contexto:
            print("Mediator")
            count = 0
            while count < len(child_files):
                mediator_list.append(child_files[count])
                count = count + 1
        if 'composite.xml' in child_files:
            print(path)
            for x in child_files:
                if 'composite.xml' in x:
                    composite = x
                    service_list.append(utils.FilesOperations.match_in_composite(path, composite))
    return service_list, mediator_list, bpels_list, operation_list

    # call_soa_generator(service_list, mediator_list, bpels_list, operation_list)


def create_dirs(path):
    os.mkdir(path)


def call_soa_generator(service, mediator, bpels, operation):
    print('print service_list')
    print(service)
    print('print mediator_list')
    print(mediator)
    print('print bpels_list')
    print(bpels)
    print('print operation_list')
    print(operation)
    print('print service_object_list')
    generator.diagram.SequenceDiagramSimpleGenerator.uml_bpel_generator(service, mediator, bpels, operation)


def call_generator(proxy, pipeline, business, operations, database, isdir):
    print('print bussines_list')
    print(business)
    print('print pipeline_list')
    print(pipeline)
    print('print proxy_list')
    print(proxy)
    print('print database_list')
    print(database)
    print('print service_object_list')

    generator.diagram.SequenceDiagramSimpleGenerator.uml_cs_generator(proxy, pipeline, business, operations, database,
                                                                      isdir)
    # generator.UmlGenerator.uml_vs_generator(proxy, pipeline, business, operations, database)
    # generator.UmlGenerator.uml_complex_generator(proxy, pipeline, business, operations, database)


if __name__ == "__main__":
    # navigate_path("Cibt-OSB-ContactEvent-DS", service_object=[])
    # navigate_path("Cibt-OSB-Country-DS", type="DS")
    # navigate_path("Cibt-OSB-Genesis-CS")
    # navigate_path('Cibt-SOA-ManageSalesCase-BAS')
    # navigate_path('Cibt-SOA-ContactEvent-BAS(Development)')
    navigate_path('Cibt-SOA-ManageModule-BAS')
    # navigate_path('Cibt-SOA-ManageCountry-BAS')
    # navigate_path('Cibt-SOA-ManageProductType-BAS')
    # navigate_path('Cibt-SOA-ManageOrganisation-BAS')