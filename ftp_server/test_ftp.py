import unittest
import roesifier
import redis


class TestRoesifier(unittest.TestCase):

    def setUp(self):
        return True

    def test_redis_connection(self):
        redis_connection = redis.StrictRedis(host='localhost', port=6379)
        redis_check = roesifier.check_redis_connection(redis_connection)
        self.assertTrue(redis_check)


if __name__ == '__main__':
    unittest.main()
