from botocore.exceptions import ClientError
from dataclasses import dataclass, field
import os

from smartrewind.backend.common import emit
from smartrewind.backend.s3 import Image, BUCKET_NAME
from smartrewind.backend.rekognition_objects import RekognitionCollectionTracking
from smartrewind.logger import Logger
from smartrewind.backend.rekognition import Rekognition
from smartrewind.progresstracker.statemachine import ProgressStateMachine

@dataclass
class Character:
    name: str
    s3: dict[str,dict[str,str]] = field(default_factory=dict)

@dataclass
class Collection:
    id: str
    arn: str

class CharacterTracking(Rekognition):
    def __init__(self, 
                 name, 
                 queue, 
                 video, 
                 rekognition_client, 
                 s3_resource, 
                 collection_id, 
                 collection_folder, 
                 results_file_name, 
                 logger: Logger,
                 progress_state_machine: ProgressStateMachine) -> None:
        super().__init__(name, queue, video, rekognition_client, logger)
        self.collection = None
        self.collection_id = collection_id
        self.results_file_name = results_file_name
        self.s3_resource = s3_resource
        self.collection_folder = collection_folder
        self.progress_state_machine = progress_state_machine

    def create_collection(self):
        try:
            emit(self.progress_state_machine, 25, "Creating collection...")
            response = self.rekognition_client.create_collection(CollectionId=self.collection_id)
            self.logger.log(
                Logger.Level.DEBUG, {
                    "response": response,
                    "api": "create_collection",
                    "params": {
                        "collection_id": self.collection_id
                    }
                }
            )
        except self.rekognition_client.exceptions.ResourceAlreadyExistsException:
            self.logger.log(Logger.Level.INFO, {
                "message": f"Collection \"{self.collection_id}\"already exists"
            })
        except ClientError as e:
            self.logger.log(Logger.Level.ERROR, {
                "message": f"Collection could not be created",
                "error": e.response,
                "api": "create_collection"
            })
            raise Exception("Create collection error")
        self.collection = Collection(self.collection_id, '')#response['CollectionArn'])

    def load_images_to_collection(self):
        should_upload = True
        directory = os.fsencode(self.collection_folder)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            emit(self.progress_state_machine, 30, f"Uploading {filename} to collection")
            if should_upload:
                s3_object = Image(self.collection_folder + '/' + filename, self.s3_resource, self.logger).get_object()
            else:
                s3_object = {"S3Object": {"Bucket": BUCKET_NAME, "Name": filename}}
            character = Character(filename.split(".")[0], s3_object)
            try:
                response = self.rekognition_client.index_faces(CollectionId=self.collection_id,
                                  Image=character.s3,
                                  ExternalImageId=character.name,
                                  MaxFaces=1,
                                  QualityFilter="LOW",
                                  DetectionAttributes=['DEFAULT'])
                self.logger.log(Logger.Level.INFO, {
                    "response": response,
                    "api": "index_faces",
                    "params": {
                        "collection_id": self.collection_id,
                        "image": character.s3,
                        "external_image_id": character.name
                    }
                })
            except ClientError as e:
                self.logger.log(Logger.Level.ERROR, {
                    "message": f"Error encountered for {filename}",
                    "error": e.response,
                    "api": "index_faces"
                })
                raise Exception(f"Index Faces error")


    def detect_faces(self):
        self.create_collection()
        self.load_images_to_collection()
        emit(self.progress_state_machine, 40, "Waiting for job completion from AWS")
        return self._do_rekognition_job(
            "person tracking",
            self.rekognition_client.start_face_search,
            self.rekognition_client.get_face_search,
            lambda response: [
                RekognitionCollectionTracking(person["Person"], person["FaceMatches"], person["Timestamp"])
                for person in response["Persons"]
            ],
            self.results_file_name,
            CollectionId=self.collection_id,
            FaceMatchThreshold=30
        )

