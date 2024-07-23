import os
import configparser

class PropertyOperations:
    def read_properties(section_property, name_property):
        config = configparser.RawConfigParser()
        property_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(property_dir)
        config.read(r'../properties/config.ini')
        get_property = config.get(section_property, name_property)
        return get_property