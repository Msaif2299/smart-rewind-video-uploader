from smartrewind.backend.sns import SNS
from smartrewind.tests.mocks.sns import MockSNSResource

def test_sns_create():
    SNS("test", MockSNSResource()).create()

def test_sns_get_topic():
    sns = SNS("test", MockSNSResource())
    topic_1 = sns.get_topic()
    topic_2 = sns.get_topic()
    assert(topic_1 == topic_2)