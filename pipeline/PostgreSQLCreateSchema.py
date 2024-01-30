import os
import psycopg2
from configparser import ConfigParser
from configurationReader import ConfigReader


class DBHandler:

    def __init__(self,config_dir:str,config_filename:str,section_name:str):
        """
        Initialize the DatabaseManager object with default config file and section.

        :param config_file: The path to the configuration file.
        :param section: The section in the configuration file containing database connection details.
        """
        self.config_dir = config_dir
        self.config_filename = config_filename
        self.section_name = section_name
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, '..', self.config_dir, self.config_filename)
        reader = ConfigReader(config_file_path)
        self.dbConfig = reader.get_section(self.section_name)

    def readDB_config(self):
        """
        Read database connection details from the configuration file.

        :return: A dictionary containing database connection parameters.
        """
        if self.dbConfig:
            return self.dbConfig
        else:
            return {}

    def connect_to_database(self):
        try:
            db_params = self.readDB_config()
            conn = psycopg2.connect(**db_params)
            print("Connected to the database")
            return conn
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
            return None

    def execute_sql_files(self, conn):
        sql_folder = "table_schema"
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



# db = DBHandler('config','config.ini','DATABASE')
# con = db.connect_to_database()
# db.execute_sql_files(con)