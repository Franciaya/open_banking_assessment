import os
from configurationReader import ConfigReader

class SchemaValidator:
    def __init__(self,section_name,reader: ConfigReader):

        self.section_name = section_name
        self.reader = reader

    def readSchema_config(self):
        
        self.schema = self.reader.get_section(self.section_name)
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