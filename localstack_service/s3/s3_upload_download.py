import os
import json
import boto3
import tempfile

from boto3.session import Session

# Inside docker use docker dns name localstack
# os.environ['LOCALSTACK_S3_ENDPOINT_URL'] = 'http://localstack:4572'

# If your connecting to the localstack outside docker use host DNS
# each aws service has its own endpoint url ensure boto3 client is configured accordingly
# you can change endpoint_url to point to any local AWS stack e.g AWS local dynamodb instance
os.environ['LOCALSTACK_S3_ENDPOINT_URL'] = 'http://localhost:4572'
os.environ['AWS_ACCESS_KEY_ID'] = 'foo'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'bar'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


if os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'):
    sqs = boto3.client("sqs", endpoint_url = os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'))
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
      "descriptio n": "United States Dollar",
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


bucket_name = 'blockchain-s3-local-bitcoin'
bucket_key = 'btc_price.json'

session = Session()
if os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'):
    s3 = session.resource("s3", endpoint_url=os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'))
else:
    s3 = session.resource("s3")
opt_file = tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False)
opt_file.write(json.dumps(body))
opt_file.flush()
reader = open(opt_file.name, mode="r", encoding="utf-8")
s3.Bucket(bucket_name).put_object(Key=bucket_key, Body=reader.read())
reader.close()
opt_file.close()
if os.path.exists(opt_file.name):
    os.remove(opt_file.name)

