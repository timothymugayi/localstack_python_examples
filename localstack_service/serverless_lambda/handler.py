import json
import datetime


def endpoint(event, context):
    current_time = datetime.datetime.now().time()
    body = {
        "message": "Hello, world",
        "eventTime": str(current_time)
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response