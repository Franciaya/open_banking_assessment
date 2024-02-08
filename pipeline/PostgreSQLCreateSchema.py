import os
import psycopg2
from configurationReader import ConfigReader


class DBHandler:

    def __init__(self,section_name:str,reader: ConfigReader):
        #Initialize the DatabaseManager object with default config file and section.
        self.section_name = section_name
        self.reader = reader

    def readDB_config(self):
        #Read database connection details from the configuration file.

        self.dbConfig = self.reader.get_section(self.section_name)
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

    def execute_sql_files(self,sql_folder: str, conn):

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