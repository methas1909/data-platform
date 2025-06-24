# Dockerfile
FROM apache/airflow:2.5.1

USER root
COPY airflow/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER airflow
