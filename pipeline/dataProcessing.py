import json
import os
import boto3
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
    injector_dependency = Injector([DependencyModule()])

    def __init__(self,config_file_path,db_section_name,duplicate_section,currency_section,schema_section):
        self.config_file_path = config_file_path
        self.currency_section = currency_section
        self.duplicate_section = duplicate_section
        self.db_section_name = db_section_name
        self.schema_section = schema_section
        

    def extract(self,script_dir,input_folder):

        self.script_dir = script_dir
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
            
        # elif location.lower() == 's3' and file_type == 'json':
        #     config_file_path = os.path.join(self.script_dir, '..', self.config_dir, self.config_filename)
        #     reader = ConfigReader(config_file_path)

        #     bucket_name = reader.get_value('S3', 'bucket_name')
        #     ws_access_key_id = reader.get_value('AWS', 'aws_access_key_id')
        #     aws_secret_access_key = reader.get_value('AWS', 'aws_secret_access_key')
            

        #     # Create an S3 client using the AWS credentials
        #     s3 = boto3.client(
        #         's3',
        #         aws_access_key_id=ws_access_key_id,
        #         aws_secret_access_key=aws_secret_access_key
        #     )

        #     # Specify the key (path) of the object you want to retrieve from the bucket
        #     obj_key = reader.get_value('S3', 'key')

        #     try:
        #         # Retrieve the object from the S3 bucket
        #         res = s3.get_object(Bucket=bucket_name, Key=obj_key)

        #         # Read the contents of the object
        #         data = res['Body'].read().decode('utf-8')

        #         # Print the data
        #         print("Data loaded from S3:")
        #         print(data)

        #         return True, data

        #     except Exception as e:
        #         print("Error:", e)

        #         return False, str(f'Error encountered: {e}')
                        
        else:   
            return False, "Invalid location or empy JSON File"
                    


    def process_data(self,data,json_root_key: str):

        self.reader = DataProcessing.injector_dependency.\
        create_object(ConfigReader,config_file_path=self.config_file_path)
        transformed_data = []
        error_data = []
        transactions = data.get(json_root_key, [])

        for record in transactions:
            try:
                transformed_record, error_record = self._process_record(record)
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
        return trans_data, error_data
    

    def _process_record(self, record):
        # instance_with_injection = injector.create_object(MyClass, file_path=file_path_value)

        allowedCur = AllowedCurrencyValidator(self.currency_section,self.reader)
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
        #print("Count after duplicate removal: ", len(filtered_data[self.transaction_key]))

        
        return filtered_data
    
    def transform_data(self,data,root_key,col_key,new_root_key):

        # Convert the extracted data to JSON format
        distinct_customers = {}

        for customer in data[root_key]:
            customer_id = customer[col_key]
            if customer_id not in distinct_customers:
                distinct_customers[customer_id] = {
                    "customer_id": customer_id,
                    "transaction_date": customer["transaction_date"]
                }

        customers_list = list(distinct_customers.values())
        customers_data = {
                new_root_key:json.loads(json.dumps(customers_list, indent=4))
        }

        return customers_data
    
    def emptyRecordDump(self,data,key):
        filtered_transactions = []
        for transaction in data[key]:
            try:
                if 'customer_id' in transaction and 'transaction_id' in transaction:
                    filtered_transactions.append(transaction)
            except TypeError as e:
                print(f"Error: {e}")

        data[key] = filtered_transactions

        return data


    def load_data_into_tables(self, data,root_key,tbl,sql_folder,filename):
        try:
            db = DBHandler(self.db_section_name,self.reader)
            conn = db.connect_to_database()
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


#(self,config_file_path,db_section_name,duplicate_section,currency_section,schema_section)
transformed_data,error_data = None,None
config_file_path = r"D:\open_banking_assessment\config\config.ini"
script_dir = r"D:\open_banking_assessment\pipeline"
processor = DataProcessing(config_file_path,'DATABASE','purge_duplicate',
                           'allowed_currencies','transactions_table_schema')

# # Process data
flag, data = processor.extract(script_dir,'input_data')
print(flag)
# print(f"Data returns {flag}")
# if flag:
#     transformed_data, error_data = processor.process_data(data)
# dup = JSONDuplicateRemover('config','config.ini','purge_duplicate')
# print("Count before duplicate removal: ", len(transformed_data['transactions']))
# dup.save_json(transformed_data,'clean_dump','transact_transformed.json')cls
# dup.save_json(error_data,'clean_dump','error_bucket.json')

#filtered_transactions_data = processor.remove_duplicates(transformed_data,'transactions_key','composite_keys','source_date_key')
#dup.save_json(filtered_transactions_data,'clean_dump','filtered_transactions_data.json')
#print("Count after duplicate removal: ", len(filtered_transactions_data['transactions']))

#transformed_customers_data = processor.transform_data(filtered_transactions_data,'transactions','customer_id')
#dup.save_json(transformed_customers_data,'clean_dump','transformed_customers_data.json')
# print("Count after duplicate removal: ", len(transformed_customers_data['customers']))
# processor.load_data_into_tables(transformed_customers_data,'customers','customers','sql','upsert_customer_query.sql')