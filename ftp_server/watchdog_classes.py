import os
import time
from roesifier import process_new_file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class OnMyWatch:

    def __init__(self):
        self.observer = Observer()
        # Set the directory on watch
        self.watch_directory = "/ftphome/tranfer_files"
        self.handler = Handler(self.watch_directory)

    def run(self):
        # define FTP path to scan all files before watchdog client
        dir_list = os.listdir(self.watch_directory)
        # scans all files in FTP dir and runs the main func before watchdog client
        for file in dir_list:
            process_new_file(file, self.watch_directory)

        #Handler.__class__.watch_directory = self.watch_directory
        event_handler = Handler(self.watch_directory)
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as error:
            self.observer.stop()

        self.observer.join()


class Handler(FileSystemEventHandler):
    watch_directory = None
    def __init__(self, watch_directory):
        self.watch_directory = watch_directory
    @staticmethod
    # action's when Event(FIle) is closed:
    def on_closed(event, **kwargs):
        if event.is_directory:
            return None
        # create variable with the name of the file
        file_name = event.src_path.replace(Handler.watch_directory, '')
        process_new_file(file_name, Handler.watch_directory)


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
