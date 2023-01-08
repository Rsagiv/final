#import modul's: time, Observer, FileSystemEventHandler,logging, redis, requests
import time
import redis
import requests
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
  

#define redis on local host, on port 6379
r=redis.StrictRedis(host='localhost', port=6379)


#define the IP of the HAProxy
url = 'http://20.224.50.228:8080'


#create a new handler and connect the logger to logs.txt file
logger = logging.getLogger('elastic')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
handler = logging.FileHandler('/home/roeihafifot/logs.txt')
logger.addHandler(handler)
  
  
class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "/ftphome/tranfer_files"
    def __init__(self):
        self.observer = Observer()
  
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
        #checking for changes every 5 seconds
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
  
        self.observer.join()
  
  
class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        #action's when Event(FIle) is created:
        elif event.event_type == 'created':
            #create variable with the name of the file
            file_name=event.src_path.replace("/ftphome/tranfer_files/", '')
            logger.info(f'success - uploaded file to FTP server: {file_name}')
            #split name by basename and extension
            split_name=file_name.split("_")
            #if half of file alradey in redis, sends both to HAProxy
            if r.exists(split_name[0]) == True:
              print("-------------------------------")
              first_half=event.src_path
              second_half=(r.get(split_name[0])).decode()
              files = []
              files.append(('files', open(first_half, 'rb')))
              files.append(('files', open(second_half, 'rb')))
              resp = requests.post(url=url, files=files)
              print("-------------------------------")
            #define first half file as Key in redis and the full path as value
            else:
              r.set(split_name[0], event.src_path, ex=60)
  
if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()