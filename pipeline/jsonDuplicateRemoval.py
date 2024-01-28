import json
from collections import defaultdict
from datetime import datetime
import configparser
from configurationReader import ConfigReader
import os

class JSONDuplicateRemover:

    def __init__(self,config_dir:str,config_filename:str,section_name:str):
        self.config_dir = config_dir
        self.config_filename = config_filename
        self.section_name = section_name

        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, '..', self.config_dir, self.config_filename)
        reader = ConfigReader(config_file_path)
        self.section_name_dict = reader.get_section(self.section_name)

    def readJSON_config(self):
        """Reads configuration from the .ini file."""
        # config = configparser.ConfigParser()
        # config.read(self.config_file)
        # return config[self.section_name]
        if self.section_name_dict:
            return self.section_name_dict
        else:
            return {}

    def load_json(self, input_file_dir,filename):
        """Loads JSON data from a file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, '..', input_file_dir, filename)

        with open(config_file_path, 'r') as file:
            data = json.load(file)
        return data

    def filter_duplicates(self, data, transaction_key, composite_keys, source_date_key):
        """Removes duplicates from JSON data based on composite keys."""
        unique_transactions = defaultdict(dict)
        for transaction in data[transaction_key]:
            composite_key = tuple(transaction[key] for key in composite_keys)
            if composite_key not in unique_transactions:
                unique_transactions[composite_key] = transaction
            else:
                current_source_date = datetime.fromisoformat(transaction[source_date_key])
                existing_source_date = datetime.fromisoformat(unique_transactions[composite_key][source_date_key])
                if current_source_date > existing_source_date:
                    unique_transactions[composite_key] = transaction
        filtered_transactions = list(unique_transactions.values())
        return {transaction_key: filtered_transactions}

    def save_json(self, data, output_file_dir,filename):
        """Saves JSON data to a file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, '..', output_file_dir, filename)

        with open(config_file_path, 'w') as file:
            json.dump(data, file, indent=4)



# rem = JSONDuplicateRemover('config', 'config.ini','purge_duplicate')
# dump_folder = 'clean_dump'
# config = rem.readJSON_config()
# transaction_key = config.get('transactions_key')
# composite_keys = config.get('composite_keys').split(',')
# source_date_key = config.get('source_date_key')

# data = rem.load_json('input_data','tech_assessment_transactions.json')
# print("Count before duplicate removal: ",len(data[transaction_key]))
# filtered_data = rem.filter_duplicates(data, transaction_key, composite_keys, source_date_key)
# print("Count after duplicate removal: ",len(filtered_data[transaction_key]))
# rem.save_json(filtered_data,dump_folder, 'curated_data.json')
# print("Duplicates removed and filtered data saved to: ", dump_folder)