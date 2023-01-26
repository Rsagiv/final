# import modul's: time, Observer, FileSystemEventHandler,logging, redis, requestsa
import redis
import requests
import final.utils.mainutils as utils

configfile = utils.import_config_file("/home/roeihafifot/config.json")

# create a new handler and connect the logger to logs.txt file
logger = utils.create_logger(configfile["LoggerName"], configfile["LogFormatter"], configfile["LogFile"])


def redis_function():
    redis_connection = redis.StrictRedis(host='localhost', port=6379)
    try:
        if redis_connection.ping():
            logger.info("SUCCESS_connection_to_redis: we've got a pong from redis!")
            return redis_connection
    except Exception:
        logger.info("cannot connect to redis: ", Exception)


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
