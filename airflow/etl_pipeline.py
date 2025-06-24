# airflow/dags/etl_pipeline.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'kkp_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for KKP data platform',
    schedule_interval='@daily',
    start_date=datetime(2025, 6, 1),
    catchup=False,
)

# Spark batch job: process bank marketing CSV
spark_batch = SparkSubmitOperator(
    task_id='spark_batch_bank_marketing',
    application='/opt/airflow/pipeline/spark_batch.py',
    conn_id='spark_default',
    dag=dag,
)

# Spark stream job: consume credit card transactions
spark_stream = SparkSubmitOperator(
    task_id='spark_stream_creditcard',
    application='/opt/airflow/pipeline/spark_stream.py',
    conn_id='spark_default',
    dag=dag,
)

spark_batch >> spark_stream