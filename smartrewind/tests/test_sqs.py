import pytest
from smartrewind.sqs import Queue
from .test_iam import MockIAMResource, MockIAMResourceErrorCases
from .test_sns import MockSNSResource
import json

class MockSQSMessage:
    def __init__(self, json_body) -> None:
        self.body = json_body
    def delete(self):
        del(self)

class MockCreatedSQSQueue:
    def __init__(self) -> None:
        self.attributes = {"QueueArn": "test"}

    def set_attributes(self, Attributes):
        self.attributes = Attributes

    def receive_messages(self, MaxNumberOfMessages, WaitTimeSeconds):
        message = json.dumps({"Message": json.dumps({"JobId": "xabc123", "Status": "SUCCEEDED"})})
        return [MockSQSMessage(message)]

class MockSQSResource:
    class exceptions:
        class QueueNameExists(BaseException):
            pass
    def __init__(self, raise_error = False) -> None:
        self.raise_error = raise_error
    def create_queue(self, QueueName, Attributes):
        if self.raise_error:
            raise self.exceptions.QueueNameExists
        return MockCreatedSQSQueue()
    
def test_sqs_create():
    Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource()).create()

def test_sqs_create_error():
    Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource(True)).create()

def test_sqs_get_notif_channel():
    q = Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource())
    q.create()
    assert(q.get_notification_channel() == {'RoleArn': 'test', 'SNSTopicArn': 'test'})

def test_sqs_poll():
    q = Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource())
    q.create()
    q.poll("xabc123")

def test_sqs_no_poll():
    with pytest.raises(RuntimeError):
        q = Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource())
        q.create()
        q.poll("xabc1234")