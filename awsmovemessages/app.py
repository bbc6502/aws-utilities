import os
from argparse import ArgumentParser
from typing import List, Dict

import boto3


def main():
    parser = ArgumentParser(description='AWS move SQS messages')
    parser.add_argument('--profile', help='AWS profile', default=os.getenv('AWS_PROFILE', 'default'))
    parser.add_argument('--region', help='AWS region', default=os.getenv('AWS_REGION', 'ap-southeast-2'))
    parser.add_argument('-s', '--source-queue-url', help='URL of the SQS queue to read messages from', required=True)
    parser.add_argument('-t', '--target-queue-url', help='URL of the SQS queue to write messages to', required=True)
    args = parser.parse_args()
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    sqs_client = session.client('sqs')
    received = sqs_client.receive_message(QueueUrl=args.source_queue_url, MaxNumberOfMessages=10)
    while 'Messages' in received:
        messages: List[Dict] = received.get('Messages', [])
        if not send_messages(sqs_client, args.source_queue_url, args.target_queue_url, messages):
            break
        received = sqs_client.receive_message(QueueUrl=args.source_queue_url, MaxNumberOfMessages=10)


def send_messages(sqs_client, source_queue_url: str, target_queue_url: str, messages: List[Dict]):
    if len(messages) < 1:
        return False
    entries = convert_messages_to_entries(messages)
    sent = sqs_client.send_message_batch(QueueUrl=target_queue_url, Entries=entries)
    sent_successes = sent.get('Successful', [])
    identifiers = [int(success['Id']) for success in sent_successes]
    entries = convert_receipt_handles(messages, identifiers)
    deleted = sqs_client.delete_message_batch(QueueUrl=source_queue_url, Entries=entries)
    delete_successes = deleted.get('Successful', [])
    print(f'{len(messages)} received, {len(sent_successes)} sent, {len(delete_successes)} deleted')
    return True


def convert_messages_to_entries(messages: List[Dict[str, str]]):
    return [
        {
            'Id': str(ident),
            'MessageBody': message['Body']
        }
        for ident, message in enumerate(messages)
    ]


def convert_receipt_handles(messages: List[Dict[str, str]], identifiers: List[int]):
    return [
        {
            'Id': str(ident),
            'ReceiptHandle': message['ReceiptHandle']
        }
        for ident, message in enumerate(messages)
        if ident in identifiers
    ]


if __name__ == '__main__':
    main()
