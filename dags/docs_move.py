from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from airflow.operators.email_operator import EmailOperator

with DAG('docs_move',
         schedule_interval=None,
         start_date=datetime(2023, 3, 6)) as dag:

    move_files = BashOperator(
        task_id='clone-mvp-repo',
        bash_command='/opt/airflow/dags/scripts/docs-deploy.sh ',
        dag=dag
    )

    send_email = EmailOperator(
        task_id='send_email',
        to='<email_address>',
        subject='docs deploy',
        html_content="Date: {{ ds }}",
        email_on_failure=True,
        dag=dag
    )

[move_files, send_email]
