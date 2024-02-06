from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dataProcessing import DataProcessing

# Specify the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email': ['francis@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DataProcessing class
data_processor = DataProcessing()

# Define the DAG
dag = DAG(
    'data_processing_workflow',
    default_args=default_args,
    description='Workflow for data processing',
    schedule_interval=timedelta(days=1),
)

# Define tasks for each method in the DataProcessing class
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=data_processor.extract,
    op_kwargs={
        'file_location': 'local',  # Specify file location
        'file_type': 'json',        # Specify file type
        'input_dir': 'input_data'   # Specify input directory
    },
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=data_processor.process_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=data_processor.transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_into_tables',
    python_callable=data_processor.load_data_into_tables,
    dag=dag,
)

# Define task dependencies
extract_task >> process_task >> transform_task >> load_task