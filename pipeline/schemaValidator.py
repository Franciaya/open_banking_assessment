from configparser import ConfigParser
import os
from configurationReader import ConfigReader

class SchemaValidator:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, '..', 'config', 'config.ini')
        reader = ConfigReader(config_file_path)
        self.schema = reader.get_section('transactions_table_schema')

    def readSchema_config(self):
        
        if self.schema:
            return self.schema
        else:
            return {}

    def validate(self, record):
        for column, datatype in self.schema.items():
            if column not in record:
                error_message = f"Missing column: {column}"
                return False, error_message
            if not isinstance(record[column], eval(datatype)):
                error_message = f"Invalid data type for column {column}: expected {datatype}, got {type(record[column])}"
                return False, error_message
        return True, None