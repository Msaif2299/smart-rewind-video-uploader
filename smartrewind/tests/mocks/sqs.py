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

    def receive_messages(self, **kwargs):
        message = json.dumps({"Message": json.dumps({"JobId": "xabc123", "Status": "SUCCEEDED"})})
        return [MockSQSMessage(message)]

class MockSQSResource:
    class exceptions:
        class QueueNameExists(BaseException):
            pass

    def __init__(self, raise_error = False) -> None:
        self.raise_error = raise_error
    def create_queue(self, **kwargs):
        if self.raise_error:
            raise self.exceptions.QueueNameExists
        return MockCreatedSQSQueue()
 