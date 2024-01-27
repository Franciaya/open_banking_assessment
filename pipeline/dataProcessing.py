import json
import os
import psycopg2
from datetime import datetime
from psycopg2 import sql
from currencyValidator import AllowedCurrencyValidator
from PostgreSQLCreateSchema import DBHandler

class DataProcessor:

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
                    'error_message': str(e)
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
            # Convert to the data types before data mapping into PostgeSQL table schema
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

        return transformed_record, None

    def load_data_into_tables(self, data, table_name):
        db = DBHandler(config_file=r'..\config\config.ini',section='DATABASE')
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
if __name__ == "__main__":
    # Initialize DataProcessor with database configuration
    db_config = {
        'dbname': 'your_dbname',
        'user': 'your_username',
        'password': 'your_password',
        'host': 'your_host',
        'port': 'your_port'
    }
    processor = DataProcessor(db_config)

    # Example JSON data
    data = [
        {
            'customerId': 1,
            'transactionId': 101,
            'transactionDate': '2023-01-01',
            'sourceDate': '2023-01-01',
            'merchantId': 1001,
            'categoryId': 2001,
            'amount': 100.0,
            'description': 'Purchase',
            'currency': 'USD'
        },
        # Add more data records as needed
    ]

    # Process data
    transformed_data, error_data = processor.process_data(data)

    # Load data into tables
    processor.load_data_into_tables(transformed_data, 'your_table_name')