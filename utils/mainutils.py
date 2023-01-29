import json
import logging


def import_config_file(json_file_path):
    try:
        with open(json_file_path) as jsonfile:
            configfile = json.load(jsonfile)
            return configfile
    except Exception:
        raise ("cannot open config file: ", Exception)


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
