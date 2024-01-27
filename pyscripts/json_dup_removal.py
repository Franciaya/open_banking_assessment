import json
from collections import defaultdict
from datetime import datetime
import configparser

class JSONDuplicateRemover:
    def __init__(self, config_file, section_name):
        self.config_file = config_file
        self.section_name = section_name

    def readJSON_config(self):
        """Reads configuration from the .ini file."""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config[self.section_name]

    def load_json(self, filename):
        """Loads JSON data from a file."""
        with open(filename, 'r') as file:
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

    def save_json(self, data, filename):
        """Saves JSON data to a file."""
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def remove_duplicates(self, json_filename, output_filename):
        """Removes duplicates from JSON file based on configuration."""
        config = self.readJSON_config()
        transaction_key = config.get('transactions_key')
        composite_keys = config.get('composite_keys').split(',')
        source_date_key = config.get('source_date_key')

        data = self.load_json(json_filename)
        filtered_data = self.filter_duplicates(data, transaction_key, composite_keys, source_date_key)
        self.save_json(filtered_data, output_filename)
        print("Duplicates removed and filtered data saved to", output_filename)

if __name__ == "__main__":
    config_file_path = r'C:\path\to\your\config.ini'
    section_name = 'your_section_name'
    json_file_path = r'C:\path\to\your\data.json'
    output_file_path = r'C:\path\to\your\filtered_data.json'

    remover = JSONDuplicateRemover(config_file_path, section_name)
    remover.remove_duplicates(json_file_path, output_file_path)