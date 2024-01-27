import configparser

class ConfigReader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

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