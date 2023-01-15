# import modul's: time, Observer, FileSystemEventHandler,logging, redis, requests
import time
import redis
import requests
import logging
import json
import os
from concurrent.futures import ProcessPoolExecutor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

with open("/home/roeihafifot/config.json") as jsonfile:
    configfile = json.load(jsonfile)

# define redis on local host, on port 6379
redis_connection = redis.StrictRedis(host='localhost', port=6379)

# define FTP path to scan all files before watchdog client
dir_list = os.listdir(configfile["FtpTransferFiles"])

# create a new handler and connect the logger to logs.txt file
logger = logging.getLogger(configfile["LoggerName"])
logger.setLevel(logging.DEBUG)
createhandler = logging.StreamHandler()
createhandler.setLevel(logging.DEBUG)
formatter = logging.Formatter(configfile["LogFormatter"])
createhandler.setFormatter(formatter)
logger.addHandler(createhandler)
handler = logging.FileHandler(configfile["LogFile"])
logger.addHandler(handler)


def check_redis(file_name):
    # split name by basename and extension
    split_name = file_name.split("_")
    # if half of file alradey in redis, sends both to HAProxy
    if redis_connection.exists(split_name[0]):
        append_to_list(file_name, split_name)
    # define first half file as Key in redis and the full path as value
    else:
        redis_connection.set(split_name[0], f'/ftphome/tranfer_files/{file_name}', ex=60)


def append_to_list(file_name, split_name):
    first_half = f'/ftphome/tranfer_files/{file_name}'
    second_half = (redis_connection.get(split_name[0])).decode()
    files = []
    files.append(('files', open(first_half, 'rb')))
    files.append(('files', open(second_half, 'rb')))
    send_to_fastAPI(files)


def send_to_fastAPI(files):
    try:
        resp = requests.post(url=configfile["HaProxyUrl"], files=files)
        if resp.status_code == 200:
            logger.info("SUCCESS: sent files to fastAPI")
        else:
            logger.info("ERROR: Failed to establish connection")
    except Exception as error:
        logger.info(f"ERROR: Failed to establish connection: because {error}")




class OnMyWatch:
    # Set the directory on watch
    watchDirectory = configfile["FtpTransferFiles"]

    def __init__(self):
        self.observer = Observer()

    def run(self):
        # scans all files in FTP dir and runs the main func before watchdog client
        for file in dir_list:
            check_redis(file)
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            # checking for changes every 5 seconds
            while True:
                time.sleep(5)
        except Exception as error:
            self.observer.stop()
            logger.info(f'observer stopped because of: {error} error')
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    # action's when Event(FIle) is closed:
    def on_closed(event):
        if event.is_directory:
            return None
        # create variable with the name of the file
        file_name = event.src_path.replace(configfile["FtpTransferFiles"], '')
        logger.info(f'success - uploaded file to FTP server: {file_name}')
        check_redis(file_name)


if __name__ == '__main__':
    watch = OnMyWatch()
    with ProcessPoolExecutor(max_workers=3) as executor:
        executor.submit(watch.run())
