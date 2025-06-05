from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta


# Função que será executada pelo PythonOperator
def hello_world():
    print("👋 Olá, Airflow! A DAG está funcionando!")


# Argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definindo a DAG
with DAG(
    dag_id='hello_world_dag',
    default_args=default_args,
    description='Uma DAG simples com PythonOperator',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags={'exemplo', 'tutorial'}
) as dag:

    # Definindo a tarefa
    hello_task = PythonOperator(
        task_id='say_hello',
        python_callable=hello_world,
    )

    # Definindo a ordem de execução (única tarefa aqui)
    hello_task
