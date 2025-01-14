import boto3
from botocore.exceptions import ClientError
from concurrent.futures import ThreadPoolExecutor

# SES Configuration
ses = boto3.client(
    'ses',
    region_name='us-east-1',
    endpoint_url='http://localhost:4566'
)

SENDER = "maxrai788@gmail.com"
CHARSET = "UTF-8"
RECIPIENTS = {f'Recipient {i}': f'maxrai{i}@gmail.com' for i in range(1, 100)}  # Generate 100 recipients

# Email content
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>Hello {name},</p>
  <p>This email was sent without using a template.</p>
</body>
</html>
"""
BODY_TEXT = """Hello {name},\r\n
This email was sent without using a template.
"""
SUBJECT = "Amazon SES Test (No Template)"


def batch_recipients(recipients, batch_size=50):
    """
    Splits recipients into batches of a specified size.
    """
    items = list(recipients.items())
    for i in range(0, len(items), batch_size):
        yield dict(items[i:i + batch_size])


def send_email(name, email):
    """
    Sends a single email with personalized content.
    """
    try:
        response = ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': [email]},
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML.format(name=name)
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT.format(name=name)
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT
                }
            }
        )
        print(f"Email sent to {email}. Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending email to {email}: {e.response['Error']['Message']}")


def send_bulk_emails(recipients, batch_size=50, max_workers=10):
    """
    Sends bulk emails in parallel, processing batches of recipients.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for batch in batch_recipients(recipients, batch_size):
            for name, email in batch.items():
                executor.submit(send_email, name, email)


if __name__ == "__main__":
    send_bulk_emails(RECIPIENTS, batch_size=50, max_workers=10)
