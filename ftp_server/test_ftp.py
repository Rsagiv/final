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

    def check_files_append(self):
        file1 = open("example_a.txt", "w").write("this is")
        file2 = open("example_b.txt", "w").write("a test")
        print(roesifier.check_key_in_redis(file1))
        print(roesifier.check_key_in_redis(file2))


if __name__ == '__main__':
    unittest.main()
