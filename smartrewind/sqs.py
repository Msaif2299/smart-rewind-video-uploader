import json
from botocore.exceptions import ClientError
from sns import SNS
from iam import IAM
from typing import Dict

class Queue:
    def __init__(self, notif_channel_name: str, iam_resource, sns_resource, sqs_resource) -> None:
        self.resource_name = notif_channel_name
        self.iam_resource = iam_resource
        self.sns_resource = sns_resource
        self.sqs_resource = sqs_resource
        self.topic: SNS|None = None
        self.queue: Queue|None = None
        self.role: IAM|None = None


    def create(self):
        self.topic = SNS(self.resource_name, self.sns_resource).get_topic()
        try:
            self.queue = self.sqs_resource.create_queue(
                QueueName=self.resource_name, Attributes={"ReceiveMessageWaitTimeSeconds": "5"}
            )
        except self.sqs_resource.exceptions.QueueNameExists:
            print(f"Queue: {self.resource_name} already exists, returning")
            return
        queue_arn = self.queue.attributes["QueueArn"]
        self.queue.set_attributes(
            Attributes={
                "Policy": json.dumps(
                    {
                        "Version": "2008-10-17",
                        "Statement": [
                            {
                                "Sid": "test-sid",
                                "Effect": "Allow",
                                "Principal": {"AWS": "*"},
                                "Action": "SQS:SendMessage",
                                "Resource": queue_arn,
                                "Condition": {
                                    "ArnEquals": {"aws:SourceArn": self.topic.arn}
                                },
                            }
                        ],
                    }
                )
            }
        )
        self.topic.subscribe(Protocol="sqs", Endpoint=queue_arn)
        self.role = IAM(self.resource_name, self.iam_resource, self.topic).get_role()

    def get_notification_channel(self) -> Dict:
        return {
            "RoleArn": self.role.arn, 
            "SNSTopicArn": self.topic.arn
        }
    
    def poll(self, job_id):
        status = None
        job_done = False
        while not job_done:
            messages = self.queue.receive_messages(
                MaxNumberOfMessages=1, WaitTimeSeconds=5
            )
            if messages:
                body = json.loads(messages[0].body)
                message = json.loads(body["Message"])
                print(f"Received message: {message}")
                if job_id != message["JobId"]:
                    raise RuntimeError
                status = message["Status"]
                print(f"Got message {str(message["JobId"])} with status {str(status)}.")
                messages[0].delete()
                job_done = True
        return status