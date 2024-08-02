class MockSNSTopic:
    def __init__(self) -> None:
        self.arn = "test"
    def subscribe(self, **kwargs):
        pass

class MockSNSResource:
    def create_topic(self, **kwargs):
        return MockSNSTopic()