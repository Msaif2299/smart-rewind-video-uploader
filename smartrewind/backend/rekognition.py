from botocore.exceptions import ClientError

from smartrewind.backend.rekognition_objects import RekognitionPerson
from smartrewind.logger import Logger

class Rekognition:
    def __init__(self, name, queue, video, rekognition_client, logger: Logger) -> None:
        self.name = name
        self.queue = queue
        self.video = video
        self.rekognition_client = rekognition_client
        self.logger = logger

    def _start_job(self, start_job_func, job_description, **kwargs):
        try:
            response = start_job_func(
                Video=self.video.get_object(),
                NotificationChannel=self.queue.get_notification_channel(),
                **kwargs
            )
            self.logger.log(Logger.Level.DEBUG, {
                "response": response,
                "params": {
                    "video": self.video.get_object(),
                    "notif_channel": self.queue.get_notification_channel(),
                    "kwargs": kwargs
                },
                "api": f"start_job_func, name:{start_job_func.__name__}"
            })
            job_id = response["JobId"]
            self.logger.log(Logger.Level.INFO, {
                "message": f"Started {job_description} job {job_id} on {self.video.name}"
            })
        except ClientError as e:
            self.logger.log(Logger.Level.ERROR, {
                "message": f"Couldn't start {job_description} on {self.video.name}",
                "error": e.response,
                "api": f"start_job_func, name:{start_job_func.__name__}"
            })
            raise Exception(f"Couldn't start {job_description} on {self.video.name}")
        return job_id
        
    def _get_rekognition_job_results(self, job_id, get_results_func, result_extractor):
        try:
            pagination_token = ''
            finished = False
            overall_results = []
            while not finished:
                response = get_results_func(JobId=job_id, NextToken=pagination_token)
                self.logger.log(Logger.Level.DEBUG, {
                    "response": response,
                    "params": {
                        "JobId": job_id,
                        "NextToken": pagination_token
                    },
                    "api": f"get_results_func, name:{get_results_func.__name__}"
                })
                self.logger.log(Logger.Level.INFO, f'Job {job_id} has status: {response["JobStatus"]}')
                results = result_extractor(response)
                for r in results:
                    overall_results.append(r)
                self.logger.log(Logger.Level.INFO, {
                    "message": f"Found {len(results)} items in {self.video.name} from {get_results_func.__name__}"
                })
                if 'NextToken' in response:
                    pagination_token = response['NextToken']
                else:
                    finished = True
        except ClientError as e:
            self.logger.log(Logger.Level.ERROR, {
                "message": f"Couldn't get items for {job_id}",
                "error": e.response,
                "api":  f"get_results_func, name:{get_results_func.__name__}"
            })
            raise Exception(f"Couldn't get items for {job_id}")
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