import boto3
from subprocess import call

access_key = "AKIAIZHM4QZ2PYAPVE6Q"
access_secret = "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"
region = "us-east-1"
middle_queue = "https://sqs.us-east-1.amazonaws.com/083630338242/DeepSightMid"

sqs = boto3.client('sqs', aws_access_key_id=access_key, aws_secret_access_key=access_secret, region_name=region)

while True:
    print("Checking...")

    if int(sqs.get_queue_attributes(QueueUrl=middle_queue,
                                    AttributeNames=['All'])['Attributes']['ApproximateNumberOfMessages']) > 0:
        response = sqs.receive_message(QueueUrl=middle_queue, AttributeNames=['SentTimestamp'], MaxNumberOfMessages=1,
                                       MessageAttributeNames=['All'], VisibilityTimeout=0, WaitTimeSeconds=0)
        print(response)

        message = response['Messages'][0]
        body = message["Body"]
        receipt_handle = message['ReceiptHandle']

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=middle_queue,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % body)

        # run shell script to retrieve image from Pi
        call(["C:\\Program Files\\Git\\git-bash.exe", "copy_image.sh"])
        # classify image and return
        call(["python", "return_response.py"])
