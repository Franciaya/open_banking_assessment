# Open Banking Pipeline Documentation
This comprehensive documentation provides a detailed overview of the Open Banking Pipeline project, including its structure, components, requirements, and usage instructions.
Building a roburst and maintainable data pipeline for processing dummy source data in JSON format, which simulates Open Banking transaction data, is the focus of this project. The workload involves conducting a few Data Quality checks on the incoming data before transforming and inserting it into two PostgreSQL tables.The project emphasizes modularity, extensibility, and automation to streamline the data processing workflow.

##  Data Pipeline Overview
The workload implemented is a data pipeline using Apache Airflow to process Open Banking transaction data provided in JSON format. The Open Banking Pipeline project aims to manage data processing tasks related to banking transactions.

## Project Requirement

The following are the requirements:
1. The pipeline performs several data quality checks on the incoming data to ensure its integrity and validity.
2. It validates the currency against a predefined list (EUR, GBP, USD) and checks for valid transaction dates in the 'YYYY-MM-DD' format.
3. Additionally, the pipeline detects and handles duplicate transaction records based on customerId and transactionId.
4. Once the data quality checks are passed, the pipeline loads the valid data into PostgreSQL tables.
5. It creates a 'transactions' table with columns mapping to the JSON fields and a 'customers' table with unique customer records and their most recent transaction dates.
6. The pipeline implements UPSERT logic when writing to the tables to ensure data integrity and consistency.
7. Furthermore, Personally Identifiable Information (PII) data is excluded from the tables to maintain privacy and compliance.
8. Any records that fail the data quality checks are logged into an error log table for further analysis and investigation.
9. Unit tests are included to verify the correctness of the data processing logic and ensure robustness against edge cases and unexpected scenarios.


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
The project directory structure is organized as follows:

config/: Contains configuration files used by the data processing scripts.

config.ini: Configuration file specifying database connection details, data processing parameters, and other settings.
scripts/: Contains Python scripts for data processing and database operations.
database_operations.py: Script for database operations such as connecting to the database and executing SQL queries.
data_processing.py: Script for processing banking transaction data, including extraction, validation, transformation, and loading.
main.py: Main script to orchestrate the data processing workflow.
sql/: Contains SQL files defining database schema and queries.
upsert_customer_query.sql: SQL file defining the upsert query for customer data.
tests/: Contains unit tests for the data processing scripts.
test_data_processing.py: Unit tests for the data processing logic.
.gitignore: Specifies files and directories to be ignored by Git version control.
README.md: Project README file providing an overview of the project and usage instructions.
requirements.txt: Lists Python dependencies required for running the project.


# Components
The project consists of the following components:

Configuration Management: Configuration settings are stored in the config.ini file, allowing easy customization of database connections, data processing parameters, and other settings.

Data Processing Scripts: Python scripts in the scripts/ directory handle various aspects of data processing, including extraction, validation, transformation, and loading. These scripts are designed to be modular and reusable.

SQL Files: SQL files in the sql/ directory define database schema and queries for creating tables and performing data operations. They facilitate the management of database operations and schema changes.

Unit Tests: Unit tests in the tests/ directory ensure the correctness and reliability of the data processing logic. They help identify and address any issues or bugs in the codebase.

# Software Requirements
The Open Banking Pipeline project has the following requirements:

Python 3.x: The project is written in Python and requires Python 3.x to run.
Apache Airflow: For workflow automation, monitoring, and scheduling of data processing tasks.
Psycopg2: Python PostgreSQL database adapter for interacting with PostgreSQL databases.
Boto3: AWS SDK for Python, required for accessing and interacting with AWS services such as S3.
Other Dependencies: Additional Python packages listed in the requirements.txt file, which can be installed using pip.

# Installation and Setup:
To set up and run the Open Banking Pipeline project, follow these steps:

1. Clone the project repository from GitHub:
          Copy code
          git clone <repository-url>
          Navigate to the project directory:


2. Copy code
          cd open_banking_pipeline
          Install Python dependencies using pip:


3.Copy code
          pip install -r requirements.txt
          Configure the config.ini file in the config/ directory with database connection details, data processing parameters, and other settings as per your requirements.

4. Ensure that Apache Airflow is installed and configured properly on your system. Refer to the Apache Airflow documentation for installation instructions.

5. Configure Apache Airflow to include the Open Banking Pipeline workflow. This typically involves defining DAGs (Directed Acyclic Graphs) to orchestrate the data processing tasks.

6. Implement and configure DAGs in Apache Airflow to include tasks for extracting, processing, and loading banking transaction data using the Python scripts provided in the scripts/ directory.

7. Configure monitoring and logging mechanisms within Apache Airflow to track the progress and performance of the data processing workflow.

# Usage
Once the project is set up and configured, you can use it to process banking transaction data as follows:

1. Start the Apache Airflow web server and scheduler to begin executing the data processing workflow defined in the DAGs.

2. For Monitoring, use the Apache Airflow UI to track the progress of individual tasks and the overall workflow execution.

3. Review logs and error messages generated during the data processing workflow to identify and address any issues or errors.

4. Use the provided Python scripts in the scripts/ directory to troubleshoot and debug data processing tasks if needed.

5. Once the data processing workflow is complete, verify that the processed data has been successfully loaded into the database and is available for analysis and reporting.
