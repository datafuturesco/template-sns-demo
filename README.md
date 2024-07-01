# Sample repo for creating SNS and SQS

This repo gives sample DAGs to create SNS topic and SQS queue on AWS, subscribe to SNS topic and show how they can be used for handling cross-DAG dependencies in an MWAA environment.

## Prerequisites

1. AWS account
2. AWS CLI
3. SNS and SQS permissions added to IAM user/ role
4. Working MWAA environment

This module assumes that you already have an AWS account setup, the IAM user and role have necessary permissions for SNS and SQS added to them.
You should have a running MWAA environment to execute the DAGs.

## Debugging

For checking if the SNS topic and SQS queues are created properly and the subscription is successful, you can run below commands on AWS CLI.
To ensure that you are using the correct IAM user to which you have added SNS and SQS permissions run below command in the terminal : - aws iam get-user

Once you are satisfied with the IAM user configuration the above command returned, run below commands for debugging the SNS and SQS created using DAGs.

1. Listing subscriptions on your SNS topic
   - aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:your-region:your-account-id:your-topic-name

If the create SNS and SQS DAG Runs are successful, you should be able to see your queue details in the output of the above command.

2. Publishing a message to SNS topic

   - aws sns publish --topic-arn arn:aws:sns:your-region:your-account-id:your-topic-name --message "Test message from CLI" --subject "Test"

3. Recieving messages from SQS Queue
   - aws sqs receive-message --queue-url https://sqs.your-region.amazonaws.com/your-account-id/your-queue-name
