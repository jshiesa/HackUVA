import boto3
import os
import model

access_key = "AKIAIZHM4QZ2PYAPVE6Q"
access_secret = "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"
region = "us-east-1"
middle_queue = "https://sqs.us-east-1.amazonaws.com/083630338242/DeepSightMid"
return_queue = "https://sqs.us-east-1.amazonaws.com/083630338242/DeepSightReturns"

sqs = boto3.client('sqs', aws_access_key_id=access_key, aws_secret_access_key=access_secret, region_name=region)

classification = model.classify()
response = sqs.send_message(
            QueueUrl=return_queue,
            MessageBody=classification
        )
