import json
import os
from collections import defaultdict
from datetime import datetime
from configurationReader import ConfigReader


class JSONDuplicateRemover:

    def __init__(self,section_name:str,reader: ConfigReader):
        #initialize config reader to read duplicate configuration section in the config.ini
        self.section_name = section_name
        self.reader = reader
        

    def readJSON_config(self):
        #Reads configuration from the .ini file.

        self.section_name_dict = self.reader.get_section(self.section_name)
        if self.section_name_dict:
            return self.section_name_dict
        else:
            return {}

    def load_json(self, input_file_dir,filename):
        #Loads JSON data from a file
        config_file_path = os.path.join(self.script_dir, '..', input_file_dir, filename)

        with open(config_file_path, 'r') as file:
            data = json.load(file)
        return data

    def filter_duplicates(self, data, transaction_key, composite_keys, source_date_key):
        #Removes duplicates from JSON data based on composite keys
        empty_list = []
        unique_transactions = defaultdict(dict)

        for transaction in data[transaction_key]:

            if transaction is not None:
                composite_key = tuple(transaction[key] for key in composite_keys)
                # print("Details: ",composite_key)
                # return None
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
        #Saves JSON data to a file
        current_dir = os.getcwd()
        config_file_path = os.path.join(current_dir,output_file_dir, filename)

        with open(config_file_path, 'w') as file:
            json.dump(data, file, indent=4)
