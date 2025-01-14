import os
import json
import uuid
import boto3

# Use the created SQS FIFO queue endpoint
os.environ['LOCALSTACK_SQS_ENDPOINT_URL'] = 'http://localhost:4566'
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

if os.environ.get('LOCALSTACK_SQS_ENDPOINT_URL'):
    sqs = boto3.client("sqs", endpoint_url=os.environ.get('LOCALSTACK_SQS_ENDPOINT_URL'))
else:
    sqs = boto3.client("sqs")

body = {
  "time": {
    "updated": "Jul 4, 2020 14:12:00 UTC",
    "updatedISO": "2020-07-04T14:12:00+00:00",
    "updateduk": "Jul 4, 2020 at 15:12 BST"
  },
  "disclaimer": "This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org",
  "bpi": {
    "USD": {
      "code": "USD",
      "rate": "9,083.8632",
      "description": "United States Dollar",
      "rate_float": 9083.8632
    },
    "BTC": {
      "code": "BTC",
      "rate": "1.0000",
      "description": "Bitcoin",
      "rate_float": 1
    }
  }
}

# Ensure the FIFO queue exists
# response = sqs.create_queue(
#     QueueName='blockchain-local-engine-input.fifo',
#     Attributes={'FifoQueue': 'true'}
# )

# Send message to SQS
response = sqs.send_message(
    QueueUrl='http://localhost:4566/000000000000/blockchain-local-engine-input.fifo',
    MessageBody=json.dumps(body),
    MessageDeduplicationId=str(uuid.uuid4()),
    MessageGroupId='blockchain',
    MessageAttributes={
        "contentType": {
            "StringValue": "application/json", "DataType": "String"}
    }
)

# WaitTimeSeconds=20 enables longer polling, reducing read cycles and costs in production
messages = sqs.receive_message(
    QueueUrl='http://localhost:4566/000000000000/blockchain-local-engine-input.fifo',
    AttributeNames=['All'], MaxNumberOfMessages=10, WaitTimeSeconds=20, VisibilityTimeout=30
)

messages = messages.get("Messages", [])

print('Total messages = {}'.format(len(messages)))

for message in messages:
    message_body = json.loads(message.get('Body'))
    print(message_body)
    # sqs.delete_message(
    #     QueueUrl='http://localhost:4566/000000000000/blockchain-local-engine-input.fifo',
    #     ReceiptHandle=message.get("ReceiptHandle")
    # )
    
    messages = sqs.receive_message(QueueUrl='http://localhost:4576/000000000000/blockchain-local-engine-input.fifo',
                                   AttributeNames=['All'], MaxNumberOfMessages=10, WaitTimeSeconds=20,
                                   VisibilityTimeout=30)

    messages = messages.get("Messages", [])

    print('Total messages remaining ={}'.format(len(messages)))

