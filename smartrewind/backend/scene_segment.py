from smartrewind.backend.rekognition import Rekognition
from smartrewind.backend.rekognition_objects import RekognitionTimelineSegmentation
from smartrewind.logger import Logger

class TimelineSegment(Rekognition):
    def __init__(self, name, queue, video, rekognition_client, results_file_name, logger: Logger) -> None:
        super().__init__(name, queue, video, rekognition_client, logger)
        self.results_file_name = results_file_name

    def segment(self):
        min_technical_cue_confidence = 80.0
        min_shot_confidence = 80.0
        max_pixel_threshold = 0.1
        min_coverage_percentage = 60
        return self._do_rekognition_job(
            "timeline segmentation",
            self.rekognition_client.start_segment_detection,
            self.rekognition_client.get_segment_detection,
            lambda response: [
                RekognitionTimelineSegmentation(response["Segments"], response["VideoMetadata"][0]["DurationMillis"])
            ],
            self.results_file_name,
            SegmentTypes=["TECHNICAL_CUE", "SHOT"],
            Filters={
                "TechnicalCueFilter": {
                    "BlackFrame": {
                        "MaxPixelThreshold": max_pixel_threshold,
                        "MinCoveragePercentage": min_coverage_percentage,
                    },
                    "MinSegmentConfidence": min_technical_cue_confidence,
                },
                "ShotFilter": {"MinSegmentConfidence": min_shot_confidence},
            }
        )
    