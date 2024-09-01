import logging
import sys
import os
from datetime import datetime

# create a log file with the name current date time +.log
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
'''
os.getcwd(): Gets the current working directory (e.g., C:/Users/admin/project).
os.path.join(): Joins the current working directory with the logs subdirectory and the LOG_FILE name.
logs_path: This is the full path to the log file,
constructed in a way that is compatible with the operating system.
'''
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
# Create folder in logs path
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,filemode='w'
)
