import final.ftp_server.roesifier as roesifier
import unittest
import redis
import os
import warnings
import final.utils.mainutils as utils


class TestRoesifier(unittest.TestCase):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        configfile = utils.import_config_file("/home/roeihafifot/config.json")
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
        redis_check = roesifier.redis_function().ping()
        self.assertTrue(redis_check)

    def test_redis_func(self):
        redis_connection = self.setUpClass()
        redis_connection.flushall()
        warnings.filterwarnings("ignore", category=ResourceWarning)
        file1name = "example_a.txt"
        file2name = "example_b.txt"
        first_check = roesifier.process_new_file(file1name)
        second_check = roesifier.process_new_file(file2name)
        self.assertIsNone(first_check)
        self.assertEqual(second_check, ('example_b.txt', ['example', 'b.txt']))

    def test_append_to_list(self):
        self.test_redis_func()
        configfile = utils.import_config_file("/home/roeihafifot/config.json")
        check = roesifier.append_to_list("example_b.txt", ['example', 'b.txt'])
        files_test_list = []
        files_test_list.append(('files', open(configfile["test_file2_path"], "rb")))
        files_test_list.append(('files', open(configfile["test_file1_path"], "rb")))
        self.assertEqual(str(check), str(files_test_list))


if __name__ == '__main__':
    unittest.main()
