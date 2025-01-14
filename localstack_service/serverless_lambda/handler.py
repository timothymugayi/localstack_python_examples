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

if __name__ == "__main__":
    # Example event and context data
    event = {}  # Replace with actual event data
    context = {}  # Replace with actual context data

    # Call the endpoint function with sample data
    response = endpoint(event, context)
    print(response)
