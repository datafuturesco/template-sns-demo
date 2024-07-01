from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime
from airflow.utils.dates import days_ago
import boto3

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# Python callable function to create SNS topic using boto3 client 
def create_sns_topic(topic_name):
    sns_client = boto3.client('sns')
    topic_response = sns_client.create_topic(Name=topic_name)
    topic_arn = topic_response['TopicArn']
    
    # Store the topic ARN in an Airflow Variable
    Variable.set("sns_test_arn", topic_arn)

    print(f'Created SNS Topic: {topic_arn}')
    
# Define DAG to create SNS topic
with DAG(
    'create_sns_topic',
    default_args=default_args,
    description='A simple DAG to create SNS Topic',
    schedule_interval=None,
    catchup=False
) as dag:

    create_topic = PythonOperator(
        task_id='create_sns_topic_task',
        python_callable=create_sns_topic,
        op_kwargs={'topic_name': 'sns_test_topic'} # provide unique topic name of your choice
    )

    create_topic

if __name__ == "__main__":
    dag.cli()