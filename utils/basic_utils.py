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

def get_extension(file_path):
    last_dot = file_path.rfind('.')
    length_path = len(file_path)
    file_name = file_path[last_dot:length_path]
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