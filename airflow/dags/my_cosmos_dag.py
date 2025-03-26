from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles.trino import TrinoBaseProfileMapping

from datetime import datetime

profile_config = ProfileConfig(
    profile_name="datalakehouse",
    target_name="dev",
    profile_mapping=TrinoBaseProfileMapping(
        conn_id="trino_db",
        profile_args={"database": "nessie", "schema": "raw"},
    ),
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        "/root/airflow/dags/dbt",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path="/root/airflow/dbt_venv/bin/dbt",
    ),
    # normal dag parameters
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    dag_id="my_cosmos_dag",
    default_args={"retries": 2},
)
