from smartrewind.logger import Logger

class SNS:
    def __init__(self, name, resource, logger: Logger) -> None:
        self.topic_name = name
        self.resource = resource
        self.topic = None
        self.logger = logger

    def create(self):
        topic = self.resource.create_topic(Name=self.topic_name)
        self.logger.log(Logger.Level.INFO, {
            "message": f"SNS Topic created",
            "topic": topic
        })
        return topic

    def get_topic(self):
        if self.topic is None:
            self.topic = self.create()
        return self.topic