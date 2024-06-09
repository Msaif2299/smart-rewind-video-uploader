from rekognition import Rekognition
from dataclasses import dataclass
import os
from video import Image, BUCKET_NAME
from botocore.exceptions import ClientError
from rekognition_objects import RekognitionCollectionTracking

@dataclass
class Character:
    name: str
    s3: dict

@dataclass
class Collection:
    id: str
    arn: str

class PersonTracking(Rekognition):
    def __init__(self, name, queue, video, rekognition_client, results_file_name) -> None:
        super().__init__(name, queue, video, rekognition_client)
        self.collection = None
        self.collection_id = "aphasia-sample1"
        self.results_file_name = results_file_name

    def create_collection(self):
        try:
            response = self.rekognition_client.create_collection(CollectionId=self.collection_id)
        except self.rekognition_client.exceptions.ResourceAlreadyExistsException:
            print(f"Collection \"{self.collection_id}\"already exists")
        self.collection = Collection(self.collection_id, '')#response['CollectionArn'])

    def load_images_to_collection(self):
        should_upload = True
        directory_path = "C:/Users/Mohammad Saif/Documents/Masters/MSc Project/video_metadata_generator/smartrewind/assets/sample_collection"
        directory = os.fsencode(directory_path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if should_upload:
                s3_object = Image(directory_path + '/' + filename).get_object()
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
            except ClientError as e:
                print(f"Error encountered for {filename}: {e}")
            with open("C:/Users/Mohammad Saif/Documents/Masters/MSc Project/video_metadata_generator/smartrewind/assets/api_response_index_faces_" + character.name + ".txt", "w") as f:
                print(response, file=f)


    def detect_faces(self):
        self.create_collection()
        self.load_images_to_collection()
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

