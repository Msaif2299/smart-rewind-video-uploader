from botocore.exceptions import ClientError
from smartrewind.backend.rekognition_objects import RekognitionPerson
class Rekognition:
    def __init__(self, name, queue, video, rekognition_client) -> None:
        self.name = name
        self.queue = queue
        self.video = video
        self.rekognition_client = rekognition_client

    def _start_job(self, start_job_func, job_description, **kwargs):
        try:
            response = start_job_func(
                Video=self.video.get_object(),
                NotificationChannel=self.queue.get_notification_channel(),
                **kwargs
            )
            job_id = response["JobId"]
            print(
                "Started %s job %s on %s.", job_description, job_id, self.video.name
            )
        except ClientError:
            raise Exception(
                "Couldn't start %s job on %s.", job_description, self.video.name
            )
        else:
            return job_id
        
    def _get_rekognition_job_results(self, job_id, get_results_func, result_extractor):
        try:
            pagination_token = ''
            finished = False
            overall_results = []
            while not finished:
                response = get_results_func(JobId=job_id, NextToken=pagination_token)
                print("Job %s has status: %s.", job_id, response["JobStatus"])
                results = result_extractor(response)
                with open("C:/Users/Mohammad Saif/Documents/Masters/MSc Project/video_metadata_generator/smartrewind/assets/results-raw.txt", "w") as f:
                    print(response, file=f)
                for r in results:
                    overall_results.append(r)
                print("Found %s items in %s.", len(results), self.video.name)
                if 'NextToken' in response:
                    pagination_token = response['NextToken']
                else:
                    finished = True
        except ClientError:
            raise Exception("Couldn't get items for %s.", job_id)
        else:
            return overall_results
        
    def move_to_file(self, results, results_file_name):
        dict_results = []
        for result in results:
            dict_results.append(result.to_dict())
        with open(results_file_name, "w") as f:
            print(dict_results, file=f)
        
    def _do_rekognition_job(
        self, job_description, start_job_func, get_results_func, result_extractor, results_file_name, **kwargs
    ):
        job_id = self._start_job(start_job_func, job_description, **kwargs)
        status = self.queue.poll(job_id)
        if status == "SUCCEEDED":
            results = self._get_rekognition_job_results(
                job_id, get_results_func, result_extractor
            )
        else:
            results = []
        self.move_to_file(results=results, results_file_name=results_file_name)
        return results

    def test_person_tracking(self, results_file_name):
        return self._do_rekognition_job(
            "person tracking",
            self.rekognition_client.start_person_tracking,
            self.rekognition_client.get_person_tracking,
            lambda response: [
                RekognitionPerson(person["Person"], person["Timestamp"])
                for person in response["Persons"]
            ],
            results_file_name
        )