# import modul's: time, Observer, FileSystemEventHandler,logging, redis, requestsa
import redis
import requests
import logging
import json
#did it work roei?

def import_config_file():
    json_file_path = "/home/roeihafifot/config.json"
    try:
        with open(json_file_path) as jsonfile:
            configfile = json.load(jsonfile)
            return configfile
    except Exception:
        logger.info("cannot open config file: ", Exception)


configfile = import_config_file()


def create_logger(log_name, log_format, file_location):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    # create a new handler
    create_handler = logging.StreamHandler()
    create_handler.setLevel(logging.DEBUG)
    # create the format
    formatter = logging.Formatter(log_format)
    create_handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(create_handler)
    # add a file handler
    handler = logging.FileHandler(file_location)
    logger.addHandler(handler)
    return logger


# create a new handler and connect the logger to logs.txt file
logger = create_logger(configfile["LoggerName"], configfile["LogFormatter"], configfile["LogFile"])


def check_redis_connection(redis_connection):
    try:
        # Send a ping command to the Redis server
        response = redis_connection.ping()
        # If the server responds with a PONG message, return True
        if response:
            return True
    except redis.ConnectionError:
        # If an error occurs while trying to connect to the server, return False
        return False


def redis_function():
    redis_connection = redis.StrictRedis(host='localhost', port=6379)
    if check_redis_connection(redis_connection):
        logger.info("SUCCESS_connection_to_redis: we've got a pong from redis!")
        return redis_connection
    else:
        logger.info("ERROR_connection_to_redis: we do not have a pong from redis!")


redis_connection = redis_function()


def check_key_in_redis(file_name):
    logger.info(f'success - uploaded file to FTP server: {file_name}')
    # split name by basename and extension
    split_name = file_name.split("_")
    # if half of file alradey in redis, sends both to HAProxy
    if redis_connection.exists(split_name[0]):
        append_to_list(file_name, split_name)
        return file_name, split_name
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
    return files


def send_to_fastAPI(files):
    try:
        resp = requests.post(url=configfile["HaProxyUrl"], files=files)
        if resp.status_code == 200:
            logger.info("SUCCESS: sent files to fastAPI")
        else:
            logger.info("ERROR: Failed to establish connection")
    except Exception as error:
        logger.info(f"ERROR: Failed to establish connection: because {error}")