import boto3, os
a = True
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/083630338242/HackTJ'
objects_url = "https://sqs.us-east-1.amazonaws.com/083630338242/Objects"
while (True):
    print(sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['All'])['Attributes']['ApproximateNumberOfMessages'])
    if (int(sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['All'])['Attributes']['ApproximateNumberOfMessages']) > 0):
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

        message = response['Messages'][0]
        body = response['Messages'][0]["Body"]
        receipt_handle = message['ReceiptHandle']

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % body)

        #highest = os.system('./tensorflow/classify.sh')
        highest = os.popen('./tensorflow/classify.sh').read()
        print(highest.rstrip("\n"))
        response = sqs.send_message(
            QueueUrl=objects_url,
            MessageBody=highest,
            DelaySeconds=1,
        )
        break

'''
response = client.receive_message(QueueUrl=queue_url)
if response["Messages"][0]["Body"] is "true":
    identified_object = subprocess.call(['./tensorflow/classify.sh'])
    response = client.delete_message(
    QueueUrl='string',
    ReceiptHandle='string')
'''