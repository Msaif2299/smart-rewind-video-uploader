"""
Many of the files in the "backend" package possess code from the following sources
Code Source: https://github.com/awsdocs/amazon-rekognition-developer-guide/tree/master/code_examples/
Code Source: https://docs.aws.amazon.com/rekognition/latest/dg/video-analyzing-with-sqs.html
Code Source: https://docs.aws.amazon.com/rekognition/latest/dg/faces-sqs-video.html
Code Source: https://docs.aws.amazon.com/rekognition/latest/dg/segment-example.html
"""

import os
import shutil
import boto3
from typing import Optional

from smartrewind.backend.sqs import Queue
from smartrewind.backend.s3 import Video, BUCKET_NAME
from smartrewind.backend.scene_segment import TimelineSegment
from smartrewind.backend.compressor import extract_timeslots
from smartrewind.backend.char_segment import CharacterTracking
from smartrewind.backend.common import emit
from smartrewind.progresstracker.statemachine import ProgressStateMachine
from smartrewind.logger import Logger

def process_video(
        iam_resource, 
        sns_resource, 
        sqs_resource, 
        s3_resource, 
        rekognition_client, 
        video_file_path, 
        collection_path, 
        output_metadata_file_path,
        logger: Logger,
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
    video = Video(path=video_file_path, s3_resource=s3_resource, logger=logger, object=None)#{"S3Object": {"Bucket": BUCKET_NAME, "Name": video_file_name}})
    emit(progress_state_machine, 15, "Creating SQS queue for completion notification...")
    queue = Queue(
        notif_channel_name=name, 
        iam_resource=iam_resource, 
        sns_resource=sns_resource, 
        sqs_resource=sqs_resource, 
        logger=logger)
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
        results_file_name=char_segments_results_file_path,
        logger=logger,
        progress_state_machine=progress_state_machine)
    processor.detect_faces()
    emit(progress_state_machine, 50, "Segmenting by scenes...")
    emit(progress_state_machine, 50, "Waiting for job completion from AWS...")
    processor = TimelineSegment(
        name=name, 
        queue=queue, 
        video=video, 
        rekognition_client=rekognition_client, 
        results_file_name=scene_segments_results_file_path,
        logger=logger)
    processor.segment()
    emit(progress_state_machine, 75, "Merging data from character and scene segmenting...")
    extract_timeslots(char_segments_results_file_path, scene_segments_results_file_path, output_metadata_file_path)
    emit(progress_state_machine, 90, "Deleting temporary files...")
    try:
        shutil.rmtree(directory_path)
    except OSError as e:
        logger.log(Logger.Level.ERROR, {
            "message": f"Encountered error while deleting temp directory: {e.strerror}"
        })
    emit(progress_state_machine, 100, f"Metadata file stored in {output_metadata_file_path}...")

if __name__=="__main__":
    name = "aphasia"
    iam_resource = boto3.resource("iam")
    sns_resource = boto3.resource("sns")
    sqs_resource = boto3.resource("sqs")
    rekognition_client = boto3.client("rekognition")
    s3_resource = boto3.resource("s3", region_name='us-west-2')