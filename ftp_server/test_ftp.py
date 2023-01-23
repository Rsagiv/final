import roesifier
import unittest
import redis


class TestRoesifier(unittest.TestCase):

    def setUp(self):
        return True

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    def test_redis_connection(self):
        redis_connection = redis.StrictRedis(host='localhost', port=6379)
        redis_check = roesifier.check_redis_connection(redis_connection)
        self.assertTrue(redis_check)

    def test_check_files_append(self):
        file1 = open("/ftphome/tranfer_files/example_a.txt", "w").write("this is")
        file2 = open("/ftphome/tranfer_files/example_b.txt", "w").write("a test")
        file1name = "example_a.txt"
        file2name = "example_b.txt"
        print(roesifier.check_key_in_redis(file1name))
        print(roesifier.check_key_in_redis(file2name))


if __name__ == '__main__':
    unittest.main()
