from configparser import ConfigParser
from injector import Binder, Injector, inject, Module

class ConfigReader:

    @inject
    def __init__(self,config: ConfigParser):
        self.config = config
    
    def setConfig(self,config_file_path: str):
        self.config_file_path = config_file_path

    def readConfig(self):
        self.config.read(self.config_file_path)

    def get_section(self, section_name):
        
        #Retrieve configuration settings from the specified section.
        #section_name (str): The name of the section in the configuration file.
        
        if self.config.has_section(section_name):
            return dict(self.config[section_name])
        else:
            return {}

    def get_value(self, section_name, key):
        #Retrieve a specific configuration value from the specified section.
    
        if self.config.has_section(section_name) and self.config.has_option(section_name, key):
            return self.config.get(section_name, key)
        else:
            return None