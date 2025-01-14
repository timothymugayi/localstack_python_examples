import os
import json
import boto3
import tempfile

# If connecting to the localstack use localstack endpoint
os.environ['LOCALSTACK_S3_ENDPOINT_URL'] = 'http://localhost:4566'
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# Check if LOCALSTACK_S3_ENDPOINT_URL is set, use it for S3 client
if os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'):
    s3 = boto3.resource("s3", endpoint_url=os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'))
    s3_client = boto3.client("s3", endpoint_url=os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'))
else:
    s3 = boto3.resource("s3")
    s3_client = boto3.client("s3")

# Define the S3 bucket and key
bucket_name = 'blockchain-s3-local-bitcoin'
bucket_key = 'btc_price'

# Define the data to upload
new_data = {
  "time": {
    "updated": "Jul 5, 2020 14:12:00 UTC",
    "updatedISO": "2020-07-05T14:12:00+00:00",
    "updateduk": "Jul 5, 2020 at 15:12 BST"
  },
  "disclaimer": "This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org",
  "bpi": {
    "USD": {
      "code": "USD",
      "rate": "9,183.8632",
      "description": "United States Dollar",
      "rate_float": 9183.8632
    },
    "BTC": {
      "code": "BTC",
      "rate": "1.0000",
      "description": "Bitcoin",
      "rate_float": 1
    }
  }
}

# Fetch existing data if any
try:
    obj = s3.Object(bucket_name, bucket_key)
    existing_data = json.loads(obj.get()['Body'].read().decode('utf-8'))
except s3.meta.client.exceptions.NoSuchKey:
    existing_data = {}

# Append new data to existing data
existing_data.update(new_data)

# Create a temporary file with the updated data
opt_file = tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False)
opt_file.write(json.dumps(existing_data))
opt_file.flush()

# Upload the updated data to S3 bucket
with open(opt_file.name, mode="r", encoding="utf-8") as reader:
    s3.Bucket(bucket_name).put_object(Key=bucket_key, Body=reader.read())

opt_file.close()

# Remove the temporary file
if os.path.exists(opt_file.name):
    os.remove(opt_file.name)
