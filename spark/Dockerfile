FROM tabulario/spark-iceberg

RUN apt-get update && apt-get install nano
RUN pip install --upgrade pip
RUN pip install 'apache-airflow[spark]==2.10.2' --constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.8.txt'
RUN pip install astronomer-cosmos apache-airflow-providers-trino
RUN python -m venv dbt_venv && . dbt_venv/bin/activate && pip install --no-cache-dir dbt-core dbt-trino dbt-vertica dbt-tests-adapter && deactivate


## Adding custom Airflow config for example DAGs disabling
ADD /airflow.cfg /root/airflow/airflow.cfg

# Run the Airflow database migration to set up the database schema
RUN airflow db migrate


# Create an admin user for Airflow with the specified credentials
RUN airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@example.com

# Adding Spark default connection
RUN airflow connections add --conn-type spark  --conn-host spark://spark-iceberg --conn-port 7077 spark_default

# Copy Spark jars into jars folder
COPY /input_jars/*.jar /opt/spark/jars

# Copy Spark default configs into config folder
COPY /spark-defaults.conf /opt/spark/conf/spark-defaults.conf

#RUN dbt init -s datalakehouse
#CMD ["dbt", "init", "-s", "datalakehouse"]
