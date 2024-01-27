import configparser
import os

class ConfigReader:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)

    def get_section(self, section_name):
        """
        Retrieve configuration settings from the specified section.

        Args:
            section_name (str): The name of the section in the configuration file.

        Returns:
            dict: A dictionary containing the key-value pairs of the section's settings.
                  Returns an empty dictionary if the section does not exist.
        """
        if self.config.has_section(section_name):
            return dict(self.config[section_name])
        else:
            return {}

    def get_value(self, section_name, key):
        """
        Retrieve a specific configuration value from the specified section.

        Args:
            section_name (str): The name of the section in the configuration file.
            key (str): The key whose value needs to be retrieved.

        Returns:
            str: The value corresponding to the specified key.
                 Returns None if the section or key does not exist.
        """
        if self.config.has_section(section_name) and self.config.has_option(section_name, key):
            return self.config.get(section_name, key)
        else:
            return None
        
#Usage:
# script_dir = os.path.dirname(os.path.abspath(__file__))
# config_file_path = os.path.join(script_dir, '..', 'config', 'config.ini')

# # Create an instance of ConfigReader
# config_reader = ConfigReader(config_file_path)

# # Specify the section name
# section_name = 'DATABASE'

# # Retrieve a specific value from the specified section
# db_host = config_reader.get_value(section_name, 'host')
# print("Database Host:", db_host)       