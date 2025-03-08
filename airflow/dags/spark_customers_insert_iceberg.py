from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 6),
}

# Define the DAG
dag = DAG(
    dag_id="spark_customers_insert_iceberg",
    default_args=default_args,
    description="Submit a PySpark job for Iceberg table update using SparkSubmitOperator",
    schedule_interval=None,
    catchup=False,
)


ingest_task = SparkSubmitOperator(
    task_id="ingest_permits",
    application="/root/airflow/jobs/iceberg/customers_insert_iceberg.py",
    conn_id="spark_default",
    verbose=True,
    dag=dag,
)

ingest_task
