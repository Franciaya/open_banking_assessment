import json
import os
import psycopg2
from datetime import datetime
from psycopg2 import sql
from currencyValidator import AllowedCurrencyValidator
from PostgreSQLCreateSchema import DBHandler
from configurationReader import ConfigReader
from schemaValidator import SchemaValidator
import boto3

class DataProcessor:

    def extract(self, location='local',type='json'):

        if location.lower() == 'local' and type == 'json':
            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_file_path = os.path.join(script_dir, '..', 'input_data')
            j_files = os.listdir(json_file_path)

            if len(j_files) == 1:
                j_file = os.path.join(json_file_path,j_files[0])
                
                # Open the JSON file and read its contents
                with open(j_files, 'r') as file:
                    data = json.load(file)

                return True, data

            else:
                return False, "Empty or to many files in the directory"
            
        elif location.lower() == 's3' and type == 'json':
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_file_path = os.path.join(script_dir, '..', 'input_data','config.ini')
            reader = ConfigReader(config_file_path)

            ws_access_key_id = reader.get_value('AWS','aws_access_key_id')
            aws_secret_access_key = reader.get_value('AWS','aws_secret_access_key')
            bucket_name = reader.get_value('S3','bucket_name')

            # Create an S3 client using the AWS credentials
            s3 = boto3.client(
                's3',
                aws_access_key_id=ws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )

            # Specify the key (path) of the object you want to retrieve from the bucket
            obj_key = reader.get_value('S3','key')

            try:
                # Retrieve the object from the S3 bucket
                res = s3.get_object(Bucket=bucket_name, Key=obj_key)

                # Read the contents of the object
                data = res['Body'].read().decode('utf-8')

                # Print the data
                print("Data loaded from S3:")
                print(data)

                return True, data

            except Exception as e:
                print("Error:", e)

                return False, str(f'Error encountered: {e}')
                        
        else:   
            return False, "Invalid location or type"
                    


    def process_data(self, data):
        transformed_data = []
        error_data = []

        for record in data:
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

        return transformed_data, error_data

    def _process_record(self, record):
        allowedCur = AllowedCurrencyValidator()
        if not allowedCur.validate(record['currency']):
            return None, {
                'customer_id': record['customerId'],
                'transaction_id': record['transactionId'],
                'error_message': 'Invalid currency'
            }   

        try:
            # Convert to defined schema in config.ini before data mapping into PostgeSQL DB
            transaction_date = datetime.strptime(record['transactionDate'], '%Y-%m-%d').date()
            parsed_date = datetime.strptime(record['sourceDate'], "%Y-%m-%dT%H:%M:%S")
            source_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            amount = float(record['amount'])

        except ValueError as e:
            return None, {
                'customer_id': record['customerId'],
                'transaction_id': record['transactionId'],
                'error_message': str(f'Invalid format: {e}')
            }

        transformed_record = {
            'customer_id': record['customerId'],
            'customer_name': record['customerName'],
            'transaction_id': record['transactionId'],
            'transaction_date': transaction_date,
            'source_date': source_date,
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
    
    def _check_schema(self,record):

        schema = SchemaValidator()
        flag , err_msg = schema.validate()

        return flag, err_msg

    
    def load_data_into_tables(self, data, table_name):
        db = DBHandler()
        conn = db.connect_to_database()
        with conn.cursor() as cursor:
            for record in data:
                columns = record.keys()
                values = [record[column] for column in columns]

                with open('upsert_query.sql', 'r') as query_file:
                    upsert_query = sql.SQL(query_file.read()).format(
                        table_name=sql.Identifier(table_name),
                        columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
                        placeholders=sql.SQL(', ').join(map(sql.Placeholder, columns)),
                        update_columns=sql.SQL(', ').join(
                            sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(column), sql.Identifier(column))
                            for column in columns
                        )
                    )

                cursor.execute(upsert_query, values)

        conn.commit()
        conn.close()


# Example usage:
# if __name__ == "__main__":
#     # Initialize DataProcessor with database configuration
#     db_config = {
#         'dbname': 'your_dbname',
#         'user': 'your_username',
#         'password': 'your_password',
#         'host': 'your_host',
#         'port': 'your_port'
#     }
#     processor = DataProcessor(db_config)

#     # Example JSON data
#     data = [
#         {
#             'customerId': 1,
#             'transactionId': 101,
#             'transactionDate': '2023-01-01',
#             'sourceDate': '2023-01-01',
#             'merchantId': 1001,
#             'categoryId': 2001,
#             'amount': 100.0,
#             'description': 'Purchase',
#             'currency': 'USD'
#         },
#         # Add more data records as needed
#     ]

#     # Process data
#     transformed_data, error_data = processor.process_data(data)

#     # Load data into tables
#     processor.load_data_into_tables(transformed_data, 'your_table_name')