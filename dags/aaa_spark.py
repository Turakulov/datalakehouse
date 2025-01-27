from airflow import DAG
# from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator
# from airflow.hooks.mysql_hook import MySqlHook
# import pandas as pd
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

with DAG('ETL_Spark_example', default_args=default_args, schedule_interval=None, tags=["ucloud_example"]) as dag:

    spark_submit_bash_task = BashOperator(
        task_id='spark_submit_bash',
        bash_command='python /opt/airflow/spark/aaa.py',
        dag=dag,
    )
    spark_submit_bash_task