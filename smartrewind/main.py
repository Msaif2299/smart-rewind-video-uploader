from smartrewind.ui import launch_app
from logger import Logger

logging_folder = "./logs"
logger = Logger(logging_folder)
logger.start()
launch_app()
logger.stop()