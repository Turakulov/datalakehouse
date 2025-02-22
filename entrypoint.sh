#!/bin/sh
airflow scheduler -D & airflow webserver -p 8090 -D

после поднятия кафки:
docker network  connect kafka_default spark-iceberg

после поднятия вертики:
docker network  connect vertica_default spark-iceberg