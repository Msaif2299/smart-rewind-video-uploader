import pytest
from smartrewind.backend.sqs import Queue
from smartrewind.tests.mocks.iam import MockIAMResource, MockIAMResourceErrorCases
from smartrewind.tests.mocks.sns import MockSNSResource
from smartrewind.tests.mocks.sqs import MockSQSResource

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