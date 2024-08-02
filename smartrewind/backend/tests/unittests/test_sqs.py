import pytest

from smartrewind.backend.sqs import Queue
from smartrewind.backend.tests.mocks.mock_iam import MockIAMResource, MockIAMResourceErrorCases
from smartrewind.backend.tests.mocks.mock_sns import MockSNSResource
from smartrewind.backend.tests.mocks.mock_sqs import MockSQSResource
from smartrewind.logger import Logger

@pytest.fixture(autouse=True)
def logger():
    yield Logger("", True)

def test_sqs_create(logger: Logger):
    Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource(), logger).create()

def test_sqs_create_error(logger: Logger):
    Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource(True), logger).create()

def test_sqs_get_notif_channel(logger: Logger):
    q = Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource(), logger)
    q.create()
    assert(q.get_notification_channel() == {'RoleArn': 'test', 'SNSTopicArn': 'test'})

def test_sqs_poll(logger: Logger):
    q = Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource(), logger)
    q.create()
    q.poll("xabc123")

def test_sqs_no_poll(logger: Logger):
    with pytest.raises(RuntimeError):
        q = Queue("test", MockIAMResource(MockIAMResourceErrorCases()), MockSNSResource(), MockSQSResource(), logger)
        q.create()
        q.poll("xabc1234")