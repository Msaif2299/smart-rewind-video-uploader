from smartrewind.sns import SNS
class MockSNSTopic:
    def __init__(self) -> None:
        self.arn = "test"
    def subscribe(self, Protocol, Endpoint):
        pass
class MockSNSResource:
    def create_topic(self, Name):
        return MockSNSTopic()
    

def test_sns_create():
    SNS("test", MockSNSResource()).create()

def test_sns_get_topic():
    sns = SNS("test", MockSNSResource())
    topic_1 = sns.get_topic()
    topic_2 = sns.get_topic()
    assert(topic_1 == topic_2)