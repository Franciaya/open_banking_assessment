import os
from configurationReader import ConfigReader

class AllowedCurrencyValidator:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, '..', 'config', 'config.ini')
        reader = ConfigReader(config_file_path)
        self.allowed_currencies = [i.upper() for i in list(reader.get_section('allowed_currencies'))]

    def validate(self, currency):
        return currency in self.allowed_currencies