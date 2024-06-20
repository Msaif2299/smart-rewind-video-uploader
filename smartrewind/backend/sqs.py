import json
from typing import Dict

from smartrewind.backend.sns import SNS
from smartrewind.backend.iam import IAM
from smartrewind.logger import Logger

class Queue:
    def __init__(self, notif_channel_name: str, iam_resource, sns_resource, sqs_resource, logger: Logger) -> None:
        self.resource_name = notif_channel_name
        self.iam_resource = iam_resource
        self.sns_resource = sns_resource
        self.sqs_resource = sqs_resource
        self.topic = None
        self.queue: Queue|None = None
        self.role: IAM|None = None
        self.logger = logger


    def create(self):
        self.topic = SNS(self.resource_name, self.sns_resource, self.logger).get_topic()
        try:
            self.queue = self.sqs_resource.create_queue(
                QueueName=self.resource_name, Attributes={"ReceiveMessageWaitTimeSeconds": "5"}
            )
        except self.sqs_resource.exceptions.QueueNameExists:
            self.logger.log(Logger.Level.WARNING, {
                "message": f"Queue: {self.resource_name} already exists, returning"
            })
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
        self.role = IAM(self.resource_name, self.iam_resource, self.topic, self.logger).get_role()

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
                self.logger.log(Logger.Level.INFO, {
                    "message": f"Received message: {message}"
                })
                if job_id != message["JobId"]:
                    self.logger.log(Logger.Level.ERROR, {
                        "message": "Unknown Job ID encountered",
                        "err": f'Expected Job ID: {job_id}, found Job ID: {message["JobId"]}'
                    })
                    raise RuntimeError
                status = message["Status"]
                self.logger.log(Logger.Level.INFO, {
                    "message": f'Got message {str(message["JobId"])} with status {str(status)}'
                })
                messages[0].delete()
                job_done = True
        return status