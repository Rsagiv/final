import roesifier
import unittest
import redis
import os
import warnings
import json


def check_json_connection(json_file_path):
    try:
        with open(json_file_path) as jsonfile:
            json.load(jsonfile)
        return True
    except json.decoder.JSONDecodeError:
        return False
    except FileNotFoundError:
        return "no_file"


def import_config_file():
    json_file_path = "/home/roeihafifot/config.json"
    if check_json_connection(json_file_path):
        with open("/home/roeihafifot/config.json") as jsonfile:
            configfile = json.load(jsonfile)
            return configfile
    elif check_json_connection(json_file_path) == "no_file":
        logger.info("ERROR In finding config file")
    else:
        logger.info("ERROR Connection to JSON file failed")


class TestRoesifier(unittest.TestCase):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        configfile = import_config_file()
        redis_connection = redis.StrictRedis(host='localhost', port=6379)
        test_file1_contents = b"this is"
        file2_contents = b"a test"
        with open(configfile["test_file1_path"], "wb+") as file1:
            os.system(f'sudo chmod +x {configfile["test_file1_path"]}')
            file1.write(test_file1_contents)
        with open(configfile["test_file2_path"], "wb+") as file2:
            os.system(f'sudo chmod +x {configfile["test_file2_path"]}')
            file2.write(file2_contents)
        return redis_connection

    def test_redis_connection(self):
        redis_connection = self.setUpClass()
        redis_check = roesifier.check_redis_connection(redis_connection)
        self.assertTrue(redis_check)

    def test_check_files_append(self):
        redis_connection = self.setUpClass()
        redis_connection.flushall()
        warnings.filterwarnings("ignore", category=ResourceWarning)
        file1name = "example_a.txt"
        file2name = "example_b.txt"
        first_check = roesifier.check_key_in_redis(file1name)
        second_check = roesifier.check_key_in_redis(file2name)
        self.assertIsNone(first_check)
        self.assertEqual(second_check, ('example_b.txt', ['example', 'b.txt']))

    # def test_append_to_list(self):
    #     self.test_check_files_append()
    #     check = roesifier.append_to_list("example_b.txt", ['example', 'b.txt'])
    #     print(f'this is check: {check}')
    #     self.assertEqual(check, [('files', <_io.BufferedReader name='/ftphome/tranfer_files/example_b.txt'>), ('files', <_io.BufferedReader name='/ftphome/tranfer_files/example_a.txt'>)])

if __name__ == '__main__':
    unittest.main()
