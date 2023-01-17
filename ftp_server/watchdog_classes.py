class OnMyWatch:
    # Set the directory on watch
    watchDirectory = configfile["FtpTransferFiles"]

    def __init__(self):
        self.observer = Observer()

    def run(self):
        # scans all files in FTP dir and runs the main func before watchdog client
        for file in dir_list:
            check_key_in_redis(file)
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
        check_key_in_redis(file_name)