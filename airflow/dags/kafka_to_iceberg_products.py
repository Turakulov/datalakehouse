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
    dag_id="kafka_to_iceberg_products",
    default_args=default_args,
    description="Submit a PySpark job for Iceberg table update using SparkSubmitOperator",
    schedule_interval=None,
    catchup=False,
    tag=["iceberg", "raw"],
)

ingest_task = SparkSubmitOperator(
    task_id="ingest_task",
    application="/root/airflow/jobs/iceberg/products_insert_iceberg.py",
    conn_id="spark_default",
    verbose=True,
    dag=dag,
)

ingest_task
