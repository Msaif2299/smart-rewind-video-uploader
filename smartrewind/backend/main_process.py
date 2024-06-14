from smartrewind.backend.char_segment import CharacterTracking
import boto3
from smartrewind.backend.sqs import Queue
from smartrewind.backend.s3 import Video, BUCKET_NAME
from smartrewind.backend.scene_segment import TimelineSegment
from smartrewind.backend.compressor import extract_timeslots
import os
import shutil
from smartrewind.progresstracker.statemachine import ProgressStateMachine
from typing import Optional
import time

name = "aphasia"
iam_resource = boto3.resource("iam")
sns_resource = boto3.resource("sns")
sqs_resource = boto3.resource("sqs")
rekognition_client = boto3.client("rekognition")
s3_resource = boto3.resource("s3", region_name='us-west-2')

def emit(progress_state_machine:Optional[ProgressStateMachine], value: int, message: str):
    if progress_state_machine is not None:
        progress_state_machine.forward_progress_signal.emit(value, message)
        #test
        time.sleep(1)

def process_video(
        iam_resource, 
        sns_resource, 
        sqs_resource, 
        s3_resource, 
        rekognition_client, 
        video_file_path, 
        collection_path, 
        output_metadata_file_path,
        progress_state_machine:Optional[ProgressStateMachine]=None):
    
    name = "aphasia"
    directory_path = "./temp/"
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    scene_segments_results_file_path = directory_path+"scene-segments-results.txt"
    char_segments_results_file_path = directory_path+"char-segments-results.txt"
    video_name = video_file_path.split("/")[-1].split(".")[0]
    output_metadata_file_path = output_metadata_file_path+f"/{video_name}_metadata.txt"
    emit(progress_state_machine, 5, "Uploading video to S3...")
    video = Video(path=video_file_path, s3_resource=s3_resource, object=None)#{"S3Object": {"Bucket": BUCKET_NAME, "Name": video_file_name}})
    emit(progress_state_machine, 15, "Creating SQS queue for completion notification...")
    queue = Queue(notif_channel_name=name, iam_resource=iam_resource, sns_resource=sns_resource, sqs_resource=sqs_resource)
    queue.create()
    emit(progress_state_machine, 25, "Segmenting by character appearances...")
    processor = CharacterTracking(
        name=name, 
        queue=queue, 
        video=video, 
        rekognition_client=rekognition_client, 
        s3_resource=s3_resource, 
        collection_id=f"{name}_{video_name}",
        collection_folder=collection_path,
        results_file_name=char_segments_results_file_path)
    processor.detect_faces()
    emit(progress_state_machine, 50, "Segmenting by scenes...")
    processor = TimelineSegment(
        name=name, 
        queue=queue, 
        video=video, 
        rekognition_client=rekognition_client, 
        results_file_name=scene_segments_results_file_path)
    processor.segment()
    emit(progress_state_machine, 75, "Merging data from character and scene segmenting...")
    extract_timeslots(char_segments_results_file_path, scene_segments_results_file_path, output_metadata_file_path)
    emit(progress_state_machine, 90, "Deleting temporary files...")
    try:
        shutil.rmtree(directory_path)
    except OSError as e:
        print(f"Encountered error while deleting temp directory: {e.strerror}")
    emit(progress_state_machine, 100, f"Metadata file stored in {output_metadata_file_path}...")

if __name__=="__main__":
    name = "aphasia"
    iam_resource = boto3.resource("iam")
    sns_resource = boto3.resource("sns")
    sqs_resource = boto3.resource("sqs")
    rekognition_client = boto3.client("rekognition")
    s3_resource = boto3.resource("s3", region_name='us-west-2')