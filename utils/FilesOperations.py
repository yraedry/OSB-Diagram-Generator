import os
import re
import configparser
import bs4 as bs


def match_in_files(path, file):
    os.chdir(path)
    matches_list = []
    operation_list = []
    file = open(file, "r")
    if file.mode == 'r':
        for x in file:
            if re.findall('<con:branch name="', x):
                matches_list.append(re.search('<con:branch name="(.+?)">', x).group(1))
                print(matches_list)
            if re.findall('<property name="SchemaName" value="', x):
                matches_list.append(re.search('<property name="SchemaName" value="(.+?)"/>', x).group(1))
                print(matches_list)
            if re.findall('<property name="PackageName" value="', x):
                matches_list.append(re.search('<property name="PackageName" value="(.+?)"/>', x).group(1))
                print(matches_list)
            if re.findall('<property name="ProcedureName" value="', x):
                matches_list.append(re.search('<property name="ProcedureName" value="(.+?)"/>', x).group(1))
                print(matches_list)
    file.close()
    return matches_list


def read_files(path, file):
    print(path)
    print(os.getcwd())
    os.chdir(path)
    file = open(file, "r")
    # file.close()
    return file


def consolidate_digraph(first_file, second_file):
    consolidate_list = []
    check_start = 0
    for line_first_file in first_file.splitlines():
        line_first_file = line_first_file.replace("digraph G {", "")
        line_first_file = line_first_file.replace("}", "")
        line_first_file = line_first_file.replace("\n", "")
        line_first_file = line_first_file.replace("strict", "")
        if not "start" in line_first_file:
            consolidate_list.append(line_first_file)
        elif "start" in line_first_file and check_start < 2:
            consolidate_list.append(line_first_file)
            check_start = check_start + 1
        elif "" in line_first_file:
            print("valor sin nada")
        else:
            consolidate_list.append(line_first_file)
    for line_second_file in second_file.splitlines():
        line_second_file = line_second_file.replace("digraph G {", "")
        line_second_file = line_second_file.replace("}", "")
        line_second_file = line_second_file.replace("\n", "")
        line_second_file = line_second_file.replace("strict", "")
        if not "start" in line_second_file:
            consolidate_list.append(line_second_file)
        elif "start" in line_second_file and check_start < 2:
            consolidate_list.append(line_second_file)
            check_start = check_start + 1
        elif "" in line_second_file:
            print("valor sin nada")
        else:
            consolidate_list.append(line_second_file)
    return consolidate_list


def read_properties(section_property, name_property):
    config = configparser.RawConfigParser()
    property_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(property_dir)
    config.read(r'../Files/ConfigFile.properties')
    get_property = config.get(section_property, name_property)
    return get_property


def search_bpel_references(path, file):
    service_reference_list = []
    operation = ""
    partnerlink = ""
    os.chdir(path)
    file = open(file, "r")
    file_to_xml = bs.BeautifulSoup(file, 'lxml')
    invokes = file_to_xml.find_all('invoke')
    for invoke in invokes:
        operation = invoke['operation']
        partnerlink = invoke['partnerlink']
        service_reference_list.append(partnerlink)
        service_reference_list.append(operation)
        print(service_reference_list)
    file.close()
    return service_reference_list


def match_in_composite(path, file):
    service_name = ""
    os.chdir(path)
    file = open(file, "r")
    file_to_xml = bs.BeautifulSoup(file, 'lxml')
    composite = file_to_xml.find_all('composite')
    for composite_attr in composite:
        service_name = composite_attr['name']
        print(service_name)
    file.close()
    return service_name

if __name__ == "__main__":
    # navigate_path("Cibt-OSB-ContactEvent-DS", service_object=[])
    # navigate_path("Cibt-OSB-Country-DS", type="DS")
    # navigate_path("Cibt-OSB-Genesis-CS")
    search_bpel_references(r'C:\GIT\test\Cibt-SOA-ContactEvent-BAS(Development)\ContactEventBAS\SOA\BPEL', 'GetContactEventListImplProcess.bpel')