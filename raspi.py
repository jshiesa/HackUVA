import boto3
import os
import time
import model

access_key = "AKIAIZHM4QZ2PYAPVE6Q"
access_secret = "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"
region = "us-east-1"
queue_url = "https://sqs.us-east-1.amazonaws.com/083630338242/DeepSight"


def pop_message(client, url):
    response = client.receive_message(QueueUrl=url, MaxNumberOfMessages=10)

    # last message posted becomes messages
    message = response['Messages'][0]['Body']
    receipt = response['Messages'][0]['ReceiptHandle']
    client.delete_message(QueueUrl=url, ReceiptHandle=receipt)
    return message


# client = boto3.client('sqs', aws_access_key_id=access_key, aws_secret_access_key=access_secret, region_name = region)
sqs = boto3.client('sqs', aws_access_key_id=access_key, aws_secret_access_key=access_secret, region_name=region)

# waittime = 20
# client.set_queue_attributes(QueueUrl=queue_url, Attributes={'ReceiveMessageWaitTimeSeconds': str(waittime)})

# time_start = time.time()
# while time.time() - time_start < 60:
while True:
    print("Checking...")

    if int(sqs.get_queue_attributes(QueueUrl=queue_url,
                                    AttributeNames=['All'])['Attributes']['ApproximateNumberOfMessages']) > 0:
        # message = pop_message(sqs, queue_url)
        # print(message)
        response = sqs.receive_message(QueueUrl=queue_url, AttributeNames=['SentTimestamp'], MaxNumberOfMessages=1,
                                       MessageAttributeNames=['All'], VisibilityTimeout=0, WaitTimeSeconds=0)

        message = response['Messages'][0]
        body = message["Body"]
        receipt_handle = message['ReceiptHandle']

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % body)

        # take image
        classification = model.classify()
        print(classification)
        break
