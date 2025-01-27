#!/bin/sh
airflow scheduler -D & airflow webserver -p 8090 -D