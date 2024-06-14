class SNS:
    def __init__(self, name, resource) -> None:
        self.topic_name = name
        self.resource = resource
        self.topic = None

    def create(self):
        topic = self.resource.create_topic(Name=self.topic_name)
        return topic

    def get_topic(self):
        if self.topic is None:
            self.topic = self.create()
        return self.topic