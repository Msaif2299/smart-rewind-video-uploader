import os
import shutil

from smartrewind.logger import Logger

def test_basic():
    foldername = "./temp_logs"
    log = Logger(foldername)
    log_str = ""
    f_read = ""
    log.start()
    for x in range(1):
        str_val = f"testing {x}"
        log.log(Logger.Level.DEBUG, str_val)
        log_str = log_str + str_val
    log.stop()
    for fname in os.listdir(foldername):
        with open(f"{foldername}/{fname}", "r") as f:
            f_read = f.read()
    shutil.rmtree(foldername)
    clean_msg = f_read.split('\n')[0].split('] ')[-1]
    assert(f'"{log_str}"' == clean_msg)