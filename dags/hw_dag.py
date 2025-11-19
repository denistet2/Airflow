import datetime as dt
import os
import sys

from airflow.models import DAG
from airflow.operators.python import PythonOperator

# ⚡ БЛОК НАСТРОЙКИ ПУТИ (Оставляем, он работает)
dag_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(dag_path, '..', 'airflow_hw')
sys.path.insert(0, path)
os.environ['PROJECT_PATH'] = path

# ⚡ ЗАКОММЕНТИРУЙТЕ ОБА ИМПОРТА
# ⚡ ВОЗВРАЩАЕМ РЕАЛЬНЫЕ ИМПОРТЫ
from modules.pipeline import pipeline
from modules.predict import predict

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(
        dag_id='car_price_prediction',
        schedule="00 15 * * *",
        default_args=args,
) as dag:
    # ⚡ ВОЗВРАТ РЕАЛЬНОЙ ФУНКЦИИ
    pipeline_task = PythonOperator(
        task_id='pipeline',
        python_callable=pipeline,
    )

    # ⚡ ВОЗВРАТ РЕАЛЬНОЙ ФУНКЦИИ
    predict_task = PythonOperator(
        task_id='predict',
        python_callable=predict,
    )

    pipeline_task >> predict_task