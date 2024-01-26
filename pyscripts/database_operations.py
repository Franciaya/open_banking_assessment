import os
import psycopg2
from configparser import ConfigParser


class DBHandler:

    def __init__(self, config_file='config.ini', section='database'):
        """
        Initialize the DatabaseManager object with default config file and section.

        :param config_file: The path to the configuration file.
        :param section: The section in the configuration file containing database connection details.
        """

        self.config_file = config_file
        self.section = section

    def read_config(self):
        """
        Read database connection details from the configuration file.

        :return: A dictionary containing database connection parameters.
        """
        parser = ConfigParser()
        parser.read(self.config_file)

        db_params = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db_params[param[0]] = param[1]
        else:
            raise Exception(f'Section {self.section} not found in the {self.config_file} file')

        return db_params

    def connect_to_database(self):
        try:
            db_params = self.read_config()
            conn = psycopg2.connect(**db_params)
            print("Connected to the database")
            return conn
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
            return None

    def execute_sql_files(self, conn):
        sql_folder = "sql"
        sql_files = [file for file in os.listdir(sql_folder) if file.endswith('.sql')]

        if not sql_files:
            print("No SQL files found in the SQL folder")
            return

        try:
            cursor = conn.cursor()
            for file in sql_files:
                with open(os.path.join(sql_folder, file), 'r') as f:
                    sql_query = f.read()
                    cursor.execute(sql_query)
                    print(f"Executed SQL file: {file}")
            conn.commit()
            print("All SQL files executed successfully")
        except psycopg2.Error as e:
            print("Error executing SQL files:", e)
            conn.rollback()