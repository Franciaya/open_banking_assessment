# Open Banking Pipeline Documentation
This comprehensive documentation provides a detailed overview of the Open Banking Pipeline project, including its structure, components, requirements, and usage instructions.<br>
Building a roburst and maintainable data pipeline for processing dummy source data in JSON format, which simulates Open Banking transaction data, is the focus of this project. The workload involves<br> conducting a few Data Quality checks on the incoming data before transforming and inserting it into two PostgreSQL tables.The project emphasizes modularity, extensibility, and automation to streamline the data processing workflow.<br>

##  Data Pipeline Overview
The workload implemented is a data pipeline using Apache Airflow to process Open Banking transaction data provided in JSON format. The Open Banking Pipeline project aims to manage data processing tasks related to banking transactions.<br>

## Functional Requirement

The following are the requirements:<br>
1. The pipeline performs several data quality checks on the incoming data to ensure its integrity and validity.<br>
2. It validates the currency against a predefined list (EUR, GBP, USD) and checks for valid transaction dates in the 'YYYY-MM-DD' format.<br>
3. Additionally, the pipeline detects and handles duplicate transaction records based on customerId and transactionId.<br>
4. Once the data quality checks are passed, the pipeline loads the valid data into PostgreSQL tables.<br>
5. It creates a 'transactions' table with columns mapping to the JSON fields and a 'customers' table with unique customer records and their most recent transaction dates.<br>
6. The pipeline implements UPSERT logic when writing to the tables to ensure data integrity and consistency.<br>
7. Furthermore, Personally Identifiable Information (PII) data is excluded from the tables to maintain privacy and compliance.<br>
8. Any records that fail the data quality checks are logged into an error log table for further analysis and investigation.<br>
9. Unit tests are included to verify the correctness of the data processing logic and ensure robustness against edge cases and unexpected scenarios.<br>


## Workload Directory Structure
The directory structure is organized as follows:

          open_banking_pipeline/
              |-- config/
              |   |-- config.ini
              |-- scripts/
              |   |-- database_operations.py
              |   |-- data_processing.py
              |   |-- main.py
              |-- sql/
              |   |-- upsert_query.sql
              |-- tests/
              |   |-- test_data_processing.py
              |-- .gitignore
              |-- README.md
              |-- requirements.txt
              

## Folder Structure
The work directory structure is organized as follows:<br>

config/: Contains configuration files used by the data processing scripts.<br>

config.ini: Configuration file specifying database connection details, data processing parameters, and other settings.<br>
scripts/: Contains Python scripts for data processing and database operations.<br>
database_operations.py: Script for database operations such as connecting to the database and executing SQL queries.<br>
data_processing.py: Script for processing banking transaction data, including extraction, validation, transformation, and loading.<br>
main.py: Main script to orchestrate the data processing workflow.<br>
sql/: Contains SQL files defining database schema and queries.<br>
upsert_customer_query.sql: SQL file defining the upsert query for customer data.<br>
tests/: Contains unit tests for the data processing scripts.<br>
test_data_processing.py: Unit tests for the data processing logic.<br>
.gitignore: Specifies files and directories to be ignored by Git version control.<br>
README.md: Project README file providing an overview of the project and usage instructions.<br>
requirements.txt: Lists Python dependencies required for running the project.<br>


# Components
The task consists of the following components:<br>

Configuration Management: Configuration settings are stored in the config.ini file, allowing easy customization of database connections, data processing parameters, and other settings.<br>

Data Processing Scripts: Python scripts in the scripts/ directory handle various aspects of data processing, including extraction, validation, transformation, and loading. These scripts are designed to be modular and reusable.<br>

SQL Files: SQL files in the sql/ directory define database schema and queries for creating tables and performing data operations. They facilitate the management of database operations and schema changes.<br>

Unit Tests: Unit tests in the tests/ directory ensure the correctness and reliability of the data processing logic. They help identify and address any issues or bugs in the codebase.<br>

# Software Requirements
The Open Banking Pipeline has the following requirements:<br>

Python 3.x: The project is written in Python and requires Python 3.x to run.<br>
Apache Airflow: For workflow automation, monitoring, and scheduling of data processing tasks.<br>
Psycopg2: Python PostgreSQL database adapter for interacting with PostgreSQL databases.<br>
Boto3: AWS SDK for Python, required for accessing and interacting with AWS services such as S3.<br>
Other Dependencies: Additional Python packages listed in the requirements.txt file, which can be installed using pip.<br>

# Installation and Setup:
To set up and run the Open Banking Pipeline project, follow these steps:<br>

1. Clone the project repository from GitHub:<br>
          Copy code<br>
          git clone <repository-url><br>
          Navigate to the project directory:<br>


2. Copy code<br>
          cd open_banking_pipeline<br>
          Install Python dependencies using pip:<br>


 3.Copy code<br>
            pip install -r requirements.txt<br>
            Configure the config.ini file in the config/ directory with database connection details, data processing parameters, and other settings as per your requirements.<br>

4. Ensure that Apache Airflow is installed and configured properly on your system. Refer to the Apache Airflow documentation for installation instructions.<br>

5. Configure Apache Airflow to include the Open Banking Pipeline workflow. This typically involves defining DAGs (Directed Acyclic Graphs) to orchestrate the data processing tasks.<br>

6. Implement and configure DAGs in Apache Airflow to include tasks for extracting, processing, and loading banking transaction data using the Python scripts provided in the scripts/ directory.<br>

7. Configure monitoring and logging mechanisms within Apache Airflow to track the progress and performance of the data processing workflow.<br>

# Usage<br>
Once the project is set up and configured, you can use it to process banking transaction data as follows:<br>

1. Start the Apache Airflow web server and scheduler to begin executing the data processing workflow defined in the DAGs.<br>

2. For Monitoring, use the Apache Airflow UI to track the progress of individual tasks and the overall workflow execution.<br>

3. Review logs and error messages generated during the data processing workflow to identify and address any issues or errors.<br>

4. Use the provided Python scripts in the scripts/ directory to troubleshoot and debug data processing tasks if needed.<br>

5. Once the data processing workflow is complete, verify that the processed data has been successfully loaded into the database and is available for analysis and reporting.<br>
