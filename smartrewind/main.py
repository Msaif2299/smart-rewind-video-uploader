from person_tracking import CharacterTracking
import boto3
from sqs import Queue
from video import Video
from timeline_segment import TimelineSegment
from compressor import extract_timeslots
from video import BUCKET_NAME

name = "aphasia"
iam_resource = boto3.resource("iam")
sns_resource = boto3.resource("sns")
sqs_resource = boto3.resource("sqs")
rekognition_client = boto3.client("rekognition")
s3_resource = boto3.resource("s3", region_name='us-west-2')

directory_path = "C:/Users/Mohammad Saif/Documents/Masters/MSc Project/video_metadata_generator/smartrewind/assets/"
results_file_path = directory_path+"results.txt"
segments_results_file_path = directory_path+"results-segments.txt"
video_file_name = "Sample_1.mp4"
video_path = directory_path+video_file_name
video_name = video_file_name.split(".")[0]
output_metadata_file_path = directory_path+f"{video_name}_metadata.txt"

video = Video(path=directory_path+video_file_name, s3_resource=s3_resource, object=None)#{"S3Object": {"Bucket": BUCKET_NAME, "Name": video_file_name}})

queue = Queue(notif_channel_name=name, iam_resource=iam_resource, sns_resource=sns_resource, sqs_resource=sqs_resource)
queue.create()

processor = CharacterTracking(name=name, queue=queue, video=video, rekognition_client=rekognition_client, s3_resource=s3_resource, results_file_name=results_file_path)
processor.detect_faces()

processor = TimelineSegment(name=name, queue=queue, video=video, rekognition_client=rekognition_client, results_file_name=segments_results_file_path)
processor.segment()

extract_timeslots(results_file_path, segments_results_file_path, output_metadata_file_path)