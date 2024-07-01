from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
import boto3
import json

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# Python callable function to create SQS queue and subscribe to SNS topic
def create_sqs_queue_and_subscribe(queue_name):
    sqs_client = boto3.client('sqs', region_name='us-east-2')
    sns_client = boto3.client('sns', region_name='us-east-2')
    
    # Get SNS topic arn to subscribe to from airflow variables 
    topic_arn = Variable.get("sns_test_arn") # check airflow variables to get the variable value for the SNS topic
    
    # Create SQS queue
    queue = sqs_client.create_queue(QueueName=queue_name)
    
    # Get the queue URL
    queue_url = queue['QueueUrl']
    
    # Get the ARN of the queue
    queue_arn = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['QueueArn'])['Attributes']['QueueArn']
    
    # Set airflow variable
    queue_variable = queue_name + "_url"
    Variable.set(queue_variable, queue_url)
    
    # Subscribe the SQS queue to the SNS topic
    sns_client.subscribe(TopicArn=topic_arn, Protocol='sqs', Endpoint=queue_arn, Attributes={'RawMessageDelivery': 'True'})
    
    # Define the policy
    policy = {
        "Version": "2012-10-17",
        "Id": f"{queue_arn}/SQSDefaultPolicy",
        "Statement": [
            {
                "Sid": "Allow-SNS-SendMessage",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "SQS:SendMessage",
                "Resource": queue_arn,
                "Condition": {
                    "ArnEquals": {
                        "aws:SourceArn": topic_arn
                    }
                }
            }
        ]
    }
    
    # Set the policy on the SQS queue
    sqs_client.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={
            'Policy': json.dumps(policy)
        }
    )
    
    print(f'Created SQS Queue: {queue_url}')
    print(f'Subscribed SQS Queue to SNS Topic: {topic_arn}')
    print(f'Updated SQS Queue policy: {policy}')

# Define the DAG to create SQS Queue
with DAG(
    'create_sqs_queue_and_subscribe',
    default_args=default_args,
    description='A simple DAG to create SQS Queue and subscribe to SNS',
    schedule_interval=None,
    catchup=False
) as dag:

    create_queue_and_subscribe = PythonOperator(
        task_id='sqs_queue_subscribe',
        python_callable=create_sqs_queue_and_subscribe,
        op_kwargs={'queue_name': 'sqs_queue_test'} # provide the queue name to be created
    )

    create_queue_and_subscribe

if __name__ == "__main__":
    dag.cli()
