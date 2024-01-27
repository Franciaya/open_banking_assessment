from configparser import ConfigParser

class TransactionsValidator:
    def __init__(self, section:str ,config_file='config.ini'):
        self.schema = self.read_config(section, config_file)

    def read_config(self, section, config_file):
        parser = ConfigParser()
        parser.read(config_file)

        params = {}
        if parser.has_section(section):
            params = dict(parser.items(section))
        else:
            raise Exception(f'Section {section} not found in the {config_file} file')

        return params

    def validate(self, record):
        for column, datatype in self.schema.items():
            if column not in record:
                error_message = f"Missing column: {column}"
                return False, error_message
            if not isinstance(record[column], eval(datatype)):
                error_message = f"Invalid data type for column {column}: expected {datatype}, got {type(record[column])}"
                return False, error_message
        return True, None