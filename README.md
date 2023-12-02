# AWS UTILITIES #

Utilities for AWS

## Installation ##

    pip3 install --upgrade https://github.com/bbc6502/aws-utilities/archive/refs/heads/main.zip

## aws-assume-role ##

Assume an AWS role using the credentials in the specified profile

    AWS_PROFILE=default
    AWS_REGION=ap-southeast-2
    $(aws-assume-role --role role_to_assume | grep export)

## aws-move-messages ##

Move AWS SQS messages from one queue to another queue

    AWS_PROFILE=default
    AWS_REGION=ap-southeast-2
    aws-move-messages -s https://sqs.aws.com/source-queue -t https://sqs.aws.com/target-queue
