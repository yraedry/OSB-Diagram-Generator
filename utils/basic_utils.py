import re
import json

def get_file_name(file_path):
    last_slash = file_path.rfind('/')
    length_path = len(file_path)
    file_name = file_path[last_slash + 1:length_path]
    return file_name

def delete_extension(file_path):
    last_dot = file_path.rfind('.')
    file_name = file_path[:last_dot]
    return file_name

def get_last_part_value_from_character(character, file_path):
    find_character = file_path.rfind(character)
    length_path = len(file_path)
    file_name = file_path[find_character + 1:length_path]
    return file_name

def get_complete_file_name(file_path):
    last_slash = file_path.rfind('/')
    length_path = len(file_path)
    file_name = file_path[last_slash + 1:length_path]
    return file_name

def get_string_from_pattern(pattern, text):
    match = re.search(pattern, text)
    if match:
        result = match.group(1)
    else:
        result = "not found"
    return result

def create_list_from_properties(string_to_list):
    list_property = string_to_list.split(',')
    return list_property

def remove_duplicate_items(duplicate_item_list):
    return list(dict.fromkeys(duplicate_item_list))

def remove_duplicate_items_xml(duplicate_item_list):
    service_list = {}
    try:
        for service_dict in duplicate_item_list:
            if service_dict.attrib['ref'] not in service_list:
                service_list[service_dict.attrib['ref']] = get_last_part_value_from_character(':', service_dict.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'])
    except:
        print('Found service without ref')
    return service_list

def delete_with_pattern(pattern, text):
    match = re.search(pattern, text)
    if match:
        result = re.sub(pattern, '', text)
    else:
        result = "not found"
    return result

def response_json_to_xml(response_api):
    response_json = json.dumps(response_api, ensure_ascii=False)
    pattern = r'"}], ".*?}'
    response_to_xml = response_json.replace('{"lines": [{"text": "', '').replace('"}, {"text": "', '').replace('\\', '')
    response_to_xml = delete_with_pattern(pattern, response_to_xml)
    return response_to_xml

def get_node_color(file_path):
    if get_last_part_value_from_character('.', file_path) == 'proxy':
        node_color = '#dae8fc'
    elif get_last_part_value_from_character('.', file_path) == 'bix':
        node_color = '#ffe6cc'
    return node_color