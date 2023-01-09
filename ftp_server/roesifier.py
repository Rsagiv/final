# import modul's: time, Observer, FileSystemEventHandler,logging, redis, requests
import time
import redis
import multiprocessing
import requests
import logging
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

with open("/home/roeihafifot/config.json") as jsonfile:
    configfile = json.load(jsonfile)

# define redis on local host, on port 6379
Redis_connection = redis.StrictRedis(host='localhost', port=6379)

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


class OnMyWatch:
    # Set the directory on watch
    watchDirectory = configfile["FtpTransferFiles"]

    def __init__(self):
        self.observer = Observer()

    def run(self):
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
    def on_closed(event):
        if event.is_directory:
            return None
        # action's when Event(FIle) is created:
        elif event.event_type == 'closed':
            # create variable with the name of the file
            file_name = event.src_path.replace(configfile["FtpTransferFiles"], '')
            logger.info(f'success - uploaded file to FTP server: {file_name}')
            # split name by basename and extension
            split_name = file_name.split("_")
            # if half of file alradey in redis, sends both to HAProxy
            if Redis_connection.exists(split_name[0]) == True:
                print("-------------------------------")
                first_half = event.src_path
                second_half = (Redis_connection.get(split_name[0])).decode()
                files = []
                files.append(('files', open(first_half, 'rb')))
                files.append(('files', open(second_half, 'rb')))
                resp = requests.post(url=configfile["HaProxyUrl"], files=files)
                print("-------------------------------")
            # define first half file as Key in redis and the full path as value
            else:
                Redis_connection.set(split_name[0], event.src_path, ex=60)


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
