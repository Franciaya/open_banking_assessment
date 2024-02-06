import os
from configurationReader import ConfigReader

class AllowedCurrencyValidator:
    def __init__(self,section_name,reader:ConfigReader):
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # config_file_path = os.path.join(script_dir, '..', 'config', 'config.ini')
        self.reader = reader 
        self.section_name = section_name
        
    
    def readCurrency(self) -> None:
        self.allowed_currencies = [i.upper() for i in list(self.reader.get_section(self.section_name))]

    def validate(self, currency):
        return currency in self.allowed_currencies