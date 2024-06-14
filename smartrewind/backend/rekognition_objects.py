class RekognitionPerson:
    """Encapsulates an Amazon Rekognition person."""

    def __init__(self, person, timestamp=None):
        """
        Initializes the person object.

        :param person: Person data, in the format returned by Amazon Rekognition
                       functions.
        :param timestamp: The time when the person was detected, if the person
                          was detected in a video.
        """
        self.index = person.get("Index")
        self.timestamp = timestamp

    def to_dict(self):
        """
        Renders some of the person data to a dict.

        :return: A dict that contains the person data.
        """
        rendering = {}
        if self.index is not None:
            rendering["index"] = self.index
        if self.timestamp is not None:
            rendering["timestamp"] = self.timestamp
        return rendering


class RekognitionCollectionTracking:
    """Encapsulates an Amazon Rekognition person in collection tracking."""

    def __init__(self, person, facematches, timestamp=None):
        """
        Initializes the person object.

        :param person: Person data, in the format returned by Amazon Rekognition
                       functions.
        :param timestamp: The time when the person was detected, if the person
                          was detected in a video.
        """
        self.index = person.get("Index")
        self.max_similarity = 0
        self.char_name = "unknown"
        for match in facematches:
            current_similarity = match.get("Similarity")
            if self.max_similarity < current_similarity:
                self.max_similarity = current_similarity
                self.char_name = match.get("Face").get("ExternalImageId").split("-")[0]
        self.timestamp = timestamp

    def to_dict(self):
        """
        Renders some of the person data to a dict.

        :return: A dict that contains the person data.
        """
        rendering = {}
        if self.index is not None:
            rendering["index"] = self.index
        if self.timestamp is not None:
            rendering["timestamp"] = self.timestamp
        if self.max_similarity is not None:
            rendering["similarity"] = self.max_similarity
        if self.char_name is not None:
            rendering["character"] = self.char_name
        return rendering



class RekognitionTimelineSegmentation:
    def __init__(self, segments, video_duration) -> None:
        self.segments = []
        self.video_duration = video_duration
        for segment in segments:
            if segment.get("Type") == "SHOT":
                self.segments.append([segment.get("StartTimestampMillis"), segment.get("EndTimestampMillis")])

    def to_dict(self):
        """
        Renders some of the person data to a dict.

        :return: A dict that contains the person data.
        """
        return {"segments": self.segments, "total_duration": self.video_duration}
