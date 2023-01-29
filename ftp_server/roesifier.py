import redis
import requests
import final.utils.mainutils as utils

configfile = utils.import_config_file("./config.json")

# create a new handler and connect the logger to logs.txt file
logger = utils.create_logger(configfile["LoggerName"], configfile["LogFormatter"], configfile["LogFile"])


def redis_function():
    connection = redis.StrictRedis(host='localhost', port=6379)
    try:
        if connection.ping():
            logger.info("SUCCESS_connection_to_redis: we've got a pong from redis!")
            return connection
    except Exception as e:
        logger.info("cannot connect to redis: ", e)


redis_connection = redis_function()


def process_new_file(file_name, watch_directory):
    logger.info(f'success - uploaded file to FTP server: {file_name}')
    # split name by basename and extension
    split_name = file_name.split("_")
    # if half of file already in redis, sends both to HAProxy
    if redis_connection.exists(split_name[0]):
        append_to_list(file_name, split_name, watch_directory)
        return file_name, split_name
    # define first half file as Key in redis and the full path as value
    else:
        redis_connection.set(split_name[0], f'{watch_directory}/{file_name}', ex=60)


def append_to_list(file_name, split_name, watch_directory):
    first_half = f'{watch_directory}/{file_name}'
    second_half = (redis_connection.get(split_name[0])).decode()
    print(second_half)
    files = [
        ('files', open(first_half, 'rb')),
        ('files', open(second_half, 'rb'))
    ]
    send_to_fast_api(files)
    return files


def send_to_fast_api(files):
    try:
        resp = requests.post(url=configfile["HaProxyUrl"], files=files)
        if resp.status_code == 200:
            logger.info("SUCCESS: sent files to fastAPI")
        else:
            logger.info("ERROR: Failed to establish connection")
    except Exception as error:
        logger.info(f"ERROR: Failed to establish connection: because {error}")
