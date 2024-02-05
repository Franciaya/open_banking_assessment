import pytest
from airflow.models import DagBag

@pytest.fixture
def dag_bag():
    return DagBag(dag_folder='/path/to/your/dags')

def test_dag_bag_import(dag_bag):
    assert len(dag_bag.import_errors) == 0, "DAG import failures"

def test_dag_structure(dag_bag):
    dag_id = 'data_processing_workflow'
    assert dag_id in dag_bag.dags, f"Missing DAG: {dag_id}"

    dag = dag_bag.dags[dag_id]
    assert len(dag.tasks) == 4, "Incorrect number of tasks in DAG"

    task_ids = ['extract_data', 'process_data', 'transform_data', 'load_data_into_tables']
    for task_id in task_ids:
        assert task_id in dag.task_ids, f"Missing task: {task_id}"