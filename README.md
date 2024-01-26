# Project Summary
This project entails building a data pipeline for processing dummy source data in JSON format, which simulates Open Banking transaction data. The workload seeks to conduct few Data Quality checks on the incoming data prior to its transformation and insertion into two PostgreSQL tables.

#  Data Pipeline Overview
The project implements the data pipeline using AWS Glue to process Open Banking transaction data provided in JSON format. The pipeline performs several data quality checks on the incoming data to ensure its integrity and validity. It validates the currency against a predefined list (EUR, GBP, USD) and checks for valid transaction dates in the 'YYYY-MM-DD' format. Additionally, the pipeline detects and handles duplicate transaction records based on customerId and transactionId.

Once the data quality checks are passed, the pipeline loads the valid data into PostgreSQL tables. It creates a 'transactions' table with columns mapping to the JSON fields and a 'customers' table with unique customer records and their most recent transaction dates. The pipeline implements UPSERT logic when writing to the tables to ensure data integrity and consistency. Furthermore, Personally Identifiable Information (PII) data is excluded from the tables to maintain privacy and compliance.

Any records that fail the data quality checks are logged into an error log table for further analysis and investigation. Unit tests are included to verify the correctness of the data processing logic and ensure robustness against edge cases and unexpected scenarios.

# Workload Directory Structure
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
              
config/: Contains configuration files.
scripts/: Includes Python scripts for database operations and data processing.
sql/: Contains SQL files for database operations.
tests/: Holds unit tests for the data processing logic.
.gitignore: Specifies files and directories to be ignored by Git.
README.md: Project documentation.
