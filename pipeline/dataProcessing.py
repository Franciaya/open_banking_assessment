import json
import os
import boto3
import sys
import pandas as pd
from datetime import datetime, date
from psycopg2 import sql
from currencyValidator import AllowedCurrencyValidator
from PostgreSQLCreateSchema import DBHandler
from configurationReader import ConfigReader
from schemaValidator import SchemaValidator
from jsonDuplicateRemoval import JSONDuplicateRemover
from injector import Binder, Injector, inject, Module
from applicationsModule import DependencyModule


class DataProcessing:

    def __init__(self,config_path,db_section_name,duplicate_section,currency_section,schema_section):
        self.config_path = config_path
        self.currency_section = currency_section
        self.duplicate_section = duplicate_section
        self.db_section_name = db_section_name
        self.schema_section = schema_section
        

    def extract(self,script_dir,input_folder):

        self.script_dir = script_dir
        try:
            if self.script_dir:
                json_file_path = os.path.join(self.script_dir, '..', input_folder)
                j_files = os.listdir(json_file_path)

                if len(j_files) == 1:
                    j_file = os.path.join(json_file_path, j_files[0])
                    
                    # Open the JSON file and read its contents
                    with open(j_file, 'r') as file:
                        data = json.load(file)

                    return True, data

                else:
                    return False, "Empty or too many files in the directory"
                            
            else:   
                return False, "Invalid location or empy JSON File"
            
        except Exception as e:
            print(f"Error while reading file: {e}")
        
                    


    def process_data(self,data,json_root_key: str):
        injector_dependency = Injector([DependencyModule()])
        self.reader = injector_dependency.get(ConfigReader)
        self.reader.setConfig(self.config_path)
        self.reader.readConfig()
        transformed_data = []
        error_data = []
        transactions = data.get(json_root_key, [])
        # print(f"Number of record is {len(transactions)}")
        # return None,None

        for record in transactions:
            try:
                transformed_record, error_record = self._process_record(record)
                if transformed_record:
                    transformed_data.append(transformed_record)
                if error_record:
                    error_data.append(error_record)
            except Exception as e:
                error_data.append({
                    'customer_id': record.get('customerId'),
                    'transaction_id': record.get('transactionId'),
                    'error_message': str(f'Error in processing data due to: {e}')
                })
        trans_data = {

            json_root_key:json.loads(json.dumps(transformed_data))

        }
        error_log_data = {

            'errors': json.loads(json.dumps(error_data))

        }

        return trans_data, error_log_data
    

    def _process_record(self, record):
        # instance_with_injection = injector.create_object(MyClass, file_path=file_path_value)

        allowedCur = AllowedCurrencyValidator(self.currency_section,self.reader)
        allowedCur.readCurrency()
        if not allowedCur.validate(record['currency']):
            return None, {
                'customer_id': record['customerId'],
                'transaction_id': record['transactionId'],
                'error_message': 'Invalid currency'
            }   

        try:
            # Convert data type to confirm to PostgeSQL transactions table - Data Mapping
            transaction_date = datetime.strptime(record['transactionDate'], '%Y-%m-%d').date()
            parsed_date = datetime.strptime(record['sourceDate'], "%Y-%m-%dT%H:%M:%S")
            source_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            amount = float(record['amount'])

        except Exception as e:
            return None, {
                'customer_id': record['customerId'],
                'transaction_id': record['transactionId'],
                'error_message': str(f'Invalid format: {e}')
            }

        transformed_record = {
            'customer_id': record['customerId'],
            'transaction_id': record['transactionId'],
            'transaction_date': str(transaction_date),
            'source_date': str(source_date),
            'merchant_id': record['merchantId'],
            'category_id': record['categoryId'],
            'amount': amount,
            'description': record['description'],
            'currency': record['currency']
        }
        # DQ checks, schema validation 
        flag, err_msg = self._check_schema(transformed_record)

        if not flag:
            return None, {
                'customer_id': record['customerId'],
                'transaction_id': record['transactionId'],
                'error_message': err_msg
            }
        
        return transformed_record, None
    
    def _check_schema(self, record):
        #Schema checks for data type and structure to ensure DQ"""
        schema = SchemaValidator(self.schema_section,self.reader)
        schema.readSchema_config()
        flag , err_msg = schema.validate(record)

        return flag, err_msg
    
    def remove_duplicates(self, data,transactions_key, composite_keys, source_date_key):
        
        #Removes duplicates from JSON file based on configuration.
        rem = JSONDuplicateRemover(self.duplicate_section,self.reader)
        config = rem.readJSON_config()
        self.transaction_key = config.get(transactions_key)
        self.composite_keys = config.get(composite_keys).split(',')
        self.source_date_key = config.get(source_date_key)

        filtered_data = rem.filter_duplicates(data, self.transaction_key, self.composite_keys, self.source_date_key)

        
        return filtered_data
    
    def transform_data(self,data,root_key,col_key,new_root_key,date_key,*columns):

        # Convert the extracted data to JSON format
        distinct_customers = {}

        for customer in data[root_key]:
            customer_id = customer[col_key]
            if customer_id not in distinct_customers:
                distinct_customers[customer_id] = {column: customer[column] for column in columns}
            else:
                current_date = datetime.fromisoformat(customer[date_key])
                existing_date = datetime.fromisoformat(distinct_customers[customer_id][date_key])
                if current_date > existing_date:
                    distinct_customers[customer_id] = {column: customer[column] for column in columns}

        customers_list = list(distinct_customers.values())
        customers_data = {
                new_root_key:json.loads(json.dumps(customers_list, indent=4))
        }

        return customers_data
    
    def load_data(self, data,root_key,tbl,sql_folder,filename):
        try:
            db_handler = DBHandler(self.db_section_name,self.reader)
            conn = db_handler.connect_to_database()
            with conn.cursor() as cursor:
                for record in data[root_key]:   
                    columns = list(record.keys())
                    # values = [record[column] for column in columns]
                    values = list(record.values())
                    with open(os.path.join(sql_folder, filename), 'r') as query_file:
                            
                        query_template= query_file.read().strip()
                        upsert_query = sql.SQL(query_template).format(
                            table_name=sql.Identifier(tbl),
                            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
                            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
                        )
                    
                    if len(values) == len(columns):
                        # Execute the query with values
                        cursor.execute(upsert_query, values)
                    else:
                        print("Error: Number of values does not match number of columns")
                   
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {str(e)}",f" and the type of error is {type(e)}")
            conn.rollback()


if __name__ == "__main__":

    transformed_data,error_data = None,None
    config_file_path = os.path.join(os.getcwd(),'config','config.ini')
    db_schema = 'DATABASE'
    cust_table_name = 'customers'
    cust_root_key = 'customers'
    trans_table_name = 'transactions'
    trans_root_key = 'transactions'
    duplicate_section = 'purge_duplicate'
    allowed_currency = 'allowed_currencies'
    table_schema_section = 'transactions_table_schema'
    sql_folder = 'table_schema'
    script_dir = os.path.join(os.getcwd(),'pipeline')
    customer_columns = ("customer_id","transaction_date")
    
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # create depenpendency injection and read the config file
        injector_dependency = Injector([DependencyModule()])
        reader = injector_dependency.get(ConfigReader)
        reader.setConfig(config_file_path)
        reader.readConfig()
        duplicate_remover = JSONDuplicateRemover(duplicate_section,reader)

        # Connect to PostgreSQL Db and create tables transactions, customers, and error_log_tab
        db_handler = DBHandler(db_schema,reader)
        conn = db_handler.connect_to_database()
        db_handler.execute_sql_files(sql_folder,conn)

        # Process data
        processor = DataProcessing(config_file_path,db_schema,duplicate_section,
                                allowed_currency,table_schema_section)
        
        flag, data = processor.extract(script_dir,'input_data')

        if flag:
            transformed_data, error_data = processor.process_data(data,'transactions')
        
        else:
            sys.exit()

        duplicate_remover.save_json(transformed_data,'before_duplicate',f'transaction_data_transformed_{timestamp}.json')

        if len(error_data['errors']) > 0: 
            duplicate_remover.save_json(error_data,'error_dump',f'error_bucket_{timestamp}.json')

        transactions_data = processor.remove_duplicates(transformed_data,'transactions_key','composite_keys','source_date_key')
        duplicate_remover.save_json(transactions_data,'clean_dump',f'processed_transactions_data_{timestamp}.json')
        customers_data = processor.transform_data(transactions_data,'transactions','customer_id','customers','transaction_date',*customer_columns)
        duplicate_remover.save_json(customers_data,'clean_dump',f'processed_customers_data_{timestamp}.json')
        processor.load_data(customers_data,cust_root_key,cust_table_name,'sql','upsert_customer_query.sql')
        processor.load_data(transactions_data,trans_root_key,trans_table_name,'sql','upsert_transaction_query.sql')
        
        if len(error_data['errors']) > 0:
            processor.load_data_into_tables(error_data,'errors','error_log_tab','sql','insert_error_log.sql')

        print("successful!")

    except Exception as e:
        print(f"Error while trying to process data: {e}")
