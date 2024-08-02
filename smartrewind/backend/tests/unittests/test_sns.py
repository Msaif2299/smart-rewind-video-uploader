import pytest

from smartrewind.backend.sns import SNS
from smartrewind.backend.tests.mocks.mock_sns import MockSNSResource
from smartrewind.logger import Logger

@pytest.fixture(autouse=True)
def logger():
    yield Logger("", True)

def test_sns_create(logger: Logger):
    SNS("test", MockSNSResource(), logger).create()

def test_sns_get_topic(logger: Logger):
    sns = SNS("test", MockSNSResource(), logger)
    topic_1 = sns.get_topic()
    topic_2 = sns.get_topic()
    assert(topic_1 == topic_2)