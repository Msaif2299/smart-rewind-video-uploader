from queue import Queue, Empty
from threading import Thread, Lock
import os
from datetime import datetime, timezone
import json
from enum import Enum

THREAD_COUNT = 5

class Logger:
    class Level(Enum):
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
    def __init__(self, folder_loc, test_dummy=False) -> None:
        self.test_dummy = test_dummy
        if test_dummy:
            return
        self.queue = Queue(maxsize=0)
        self.lock = Lock()
        self.workers = [Thread(target=self.logEvent, args=(f"logging_thread_{idx+1}",)) for idx in range(THREAD_COUNT)]
        self.end = False
        if not os.path.exists(folder_loc) or not os.path.isdir(folder_loc):
            try:
                os.mkdir(folder_loc)
            except FileNotFoundError:
                raise Exception("Invalid folder path passed to logger")
        try:
            self.log_file = open(folder_loc + f"/log_file_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.txt", "w")
            print(os.path.abspath(self.log_file.name))
        except OSError as e:
            print(f"Error encountered while creating file: {e}")
            raise Exception("Unable to create file, maybe write access is not granted")

    def log(self, level: Level, data: dict):
        if self.test_dummy:
            return
        str_data = json.dumps(data)
        self.queue.put(f"{level}||{str_data}")

    def start(self):
        for worker in self.workers:
            worker.start()

    def stop(self):
        while not self.queue.empty():
            continue
        self.end = True
        self.queue.join()
        self.log_file.close()

    def logEvent(self, thread_name):
        print(f"Starting.... {thread_name}")
        while not self.end:
            try:
                msg = self.queue.get(timeout=1)
                with self.lock:
                    level = msg.split("||")[0]
                    body = "||".join(msg.split("||")[1:])
                    print(f"[{int(datetime.now(tz=timezone.utc).timestamp()*1000)}] [{level}] {body}", file=self.log_file)
                self.queue.task_done()
            except Empty:
                pass
            except Exception as e:
                print(f"Exception encountered: {e}")
        print(f"Stopping.... {thread_name}")