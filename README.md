# Sample repo for creating SNS and SQS

This repo gives sample DAGs to create SNS topic and SQS queue on AWS, subscribe to SNS topic and show how they can be used for handling cross-DAG dependencies in an MWAA environment.

## Prerequisites

This module assumes that you already have an AWS account setup, the IAM user and role have necessary permissions for SNS and SQS added to them.
You should have a running MWAA environment to execute the DAGs.
