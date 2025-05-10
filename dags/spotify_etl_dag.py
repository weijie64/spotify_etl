from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/scripts')
from spotify_etl import run_etl

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'spotify_etl_pipeline',
    default_args=default_args,
    description='Extract Spotify artist metadata daily',
    schedule_interval='@daily',
    catchup=False
)

task = PythonOperator(
    task_id='run_spotify_etl',
    python_callable=run_etl,
    dag=dag
)
