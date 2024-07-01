from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from datetime import datetime
import boto3

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}
 
# Define DAG to display the cross-dag dependency using SNS topic publish
with DAG(
    'sns_publish_dummy',
    default_args=default_args,
    description='A simple DAG to publish a message to an SNS topic',
    schedule_interval=None,
    catchup=False
) as dag:
    # Dummy task to show upward dag dependency success
    dummy_sleep_task = BashOperator(
        task_id='sleep_task',
        bash_command='sleep 10'
    )

    # SNS Publish operator to publish message to SNS topic after the upward tasks are successful
    publish_to_sns = SnsPublishOperator(
        task_id='publish_to_sns',
        target_arn=Variable.get("sns_test_arn"),  # SNS topic arn to which you want to publish the message
        message='This is a test message from Airflow',
        subject='Test SNS Message'
    )
    
    dummy_sleep_task >> publish_to_sns

if __name__ == "__main__":
    dag.cli()
