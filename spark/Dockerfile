FROM tabulario/spark-iceberg



RUN pip install 'apache-airflow[spark]==2.10.2' --constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.8.txt'

ADD airflow.cfg /root/airflow/airflow.cfg

# Run the Airflow database migration to set up the database schema
RUN airflow db migrate


# Create an admin user for Airflow with the specified credentials
RUN airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@example.com

#ADD entrypoint.sh /usr/local/bin/entrypoint.sh
#ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]