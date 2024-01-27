import json
import os
import psycopg2
from datetime import datetime
from psycopg2 import sql

class DataProcessor:
    def __init__(self, db_config):
        self.db_config = db_config

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
        if record['currency'] not in ['EUR', 'GBP', 'USD']:
            return None, {
                'customer_id': record['customerId'],
                'transaction_id': record['transactionId'],
                'error_message': 'Invalid currency'
            }

        try:
            transaction_date = datetime.strptime(record['transactionDate'], '%Y-%m-%d').date()
        except ValueError:
            return None, {
                'customer_id': record['customerId'],
                'transaction_id': record['transactionId'],
                'error_message': 'Invalid transactionDate'
            }

        transformed_record = {
            'customer_id': record['customerId'],
            'transaction_id': record['transactionId'],
            'transaction_date': transaction_date,
            'source_date': record['sourceDate'],
            'merchant_id': record['merchantId'],
            'category_id': record['categoryId'],
            'amount': record['amount'],
            'description': record['description'],
            'currency': record['currency']
        }

        return transformed_record, None

    def load_data_into_tables(self, data, table_name):
        conn = psycopg2.connect(**self.db_config)
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