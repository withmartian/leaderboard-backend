import boto3

from ..metrics.collect import collect_metrics_with_retries
from ..settings import settings


sqs_client = boto3.client("sqs", region_name=settings.aws_region)


async def receive_messages():
    while True:
        response = sqs_client.receive_message(
            QueueUrl=settings.aws_sqs_url,
            MaxNumberOfMessages=settings.aws_sqs_max_messages,
            WaitTimeSeconds=settings.aws_sqs_wait_time_seconds,
        )

        messages = response.get("Messages", [])
        for message in messages:
            await handle_message(message)
            sqs_client.delete_message(
                QueueUrl=settings.aws_sqs_url, ReceiptHandle=message["ReceiptHandle"]
            )


async def handle_message(message):
    print(f"Received message: {message['Body']}")
    await collect_metrics_with_retries()
