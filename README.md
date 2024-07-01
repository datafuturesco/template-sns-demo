# Sample repo for creating SNS and SQS

This repo gives sample DAGs to create SNS topic and SQS queue on AWS, subscribe to SNS topic and show how they can be used for handling cross-DAG dependencies in an MWAA environment.

## Prerequisites

1. AWS account
2. AWS CLI
3. SNS and SQS permissions added to IAM user/ role
4. Working MWAA environment

This module assumes that you already have an AWS account setup, the IAM user and role have necessary permissions for SNS and SQS added to them.
You should have a running MWAA environment to execute the DAGs.

The simple policy that can be added to IAM role to create and use the SNS ans SQS resources is given below.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSNSActions",
            "Effect": "Allow",
            "Action": [
                "sns:CreateTopic",
                "sns:DeleteTopic",
                "sns:ListTopics",
                "sns:ListSubscriptionsByTopic",
                "sns:GetSubscriptionAttributes",
                "sns:Subscribe",
                "sns:SetSubscriptionAttributes",
                "sns:ConfirmSubscription",
                "sns:Publish"
            ],
            "Resource": "arn:aws:sns:*:{AccountID}:*"
        },
        {
            "Sid": "AllowSQSActions",
            "Effect": "Allow",
            "Action": [
                "sqs:CreateQueue",
                "sqs:DeleteQueue",
                "sqs:GetQueueUrl",
                "sqs:GetQueueAttributes",
                "sqs:SetQueueAttributes",
                "sqs:ListQueues",
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage"
            ],
            "Resource": "arn:aws:sqs:*:{AccountID}:*"
        }
    ]
}

```

## Debugging

For checking if the SNS topic and SQS queues are created properly and the subscription is successful, you can run below commands on AWS CLI.
To ensure that you are using the correct IAM user to which you have added SNS and SQS permissions run below command in the terminal : `aws iam get-user`

Once you are satisfied with the IAM user configuration the above command returned, run below commands for debugging the SNS and SQS created using DAGs.

1. Listing subscriptions on your SNS topic

```
aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:your-region:your-account-id:your-topic-name
```

If the create SNS and SQS DAG Runs are successful, you should be able to see your queue details in the output of the above command.

2. Publishing a message to SNS topic

```
aws sns publish --topic-arn arn:aws:sns:your-region:your-account-id:your-topic-name --message "Test message from CLI" --subject "Test"
```

3. Recieving messages from SQS Queue

```
aws sqs receive-message --queue-url https://sqs.your-region.amazonaws.com/your-account-id/your-queue-name
```

## Cross-DAG Dependecies handling

We leveraged SNSPublish and SQSSensor operators of Airflow to achieve the cross-dag dependency.

#### create_sns_topic.py

This sample DAG creates SNS topic using boto3 client. Make sure to provide unique topic name.
The DAG also stores the topic arn as airflow variable which is used while subscribing to the topic created.

#### create_sqs_queue.py

This sample DAG creates SQS queue and also subscribes to the SNS topic.
It retrieves the SNS topic arn from the airflow variables provided in the airflow variable `sns_test_arn` to subscribe to it.
The created SQS queue url upon successful creation is also stored as airflow varibale `sqs_queue_test_url`, make sure to provide unique name to your queue.

#### sns-publish-dag.py

This DAG publishes to the SNS topic provided in the variable of `sns_test_arn` using SNSPublish operator upon successful upward dependent task runs.

#### sqs-sensor-dag.py

This is the DAG to enable cross-dag dependency, once the DAG tasks in the sns-publish-dag.py are successfully executed and the message is published to SNS topic,
SQS queues subscribed to the topic receive message. We use SQSSensor operator which waits for any such message to be received, once it reads the message from the queue url it retrieves from `sqs_queue_test` variable, it triggers the downward dependent tasks.
