import roesifier
import unittest
import redis
import os


class TestRoesifier(unittest.TestCase):

    def setUp(self):
        return True

    @classmethod
    def setUpClass(cls):
        pass

    def test_redis_connection(self):
        redis_connection = redis.StrictRedis(host='localhost', port=6379)
        redis_check = roesifier.check_redis_connection(redis_connection)
        self.assertTrue(redis_check)

    def check_files_append(self):
        file1_contents = "this is"
        file1_path = "/ftphome/transfer_files/example_a.txt"
        os.system(f"echo {file1_contents} | sudo tee {file1_path}")
        file2_contents = "a test"
        file2_path = "/ftphome/transfer_files/example_b.txt"
        os.system(f"echo {file2_contents} | sudo tee {file2_path}")
        file1name = "example_a.txt"
        file2name = "example_b.txt"
        print(roesifier.check_key_in_redis(file1name))
        print(roesifier.check_key_in_redis(file2name))

    def append_to_list(self):
        print(roesifier.append_to_list("example_a", "example"))

if __name__ == '__main__':
    unittest.main()
