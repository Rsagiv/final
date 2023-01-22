import roesifier
import unittest
import redis


class TestRoesifier(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.redis_connection = None

    @classmethod
    def setUpClass(cls):
        redis_connection = redis.StrictRedis(host='localhost', port=6379)
        return redis_connection

    def setUp(self):
        return True

    def test_redis_connection(self):
        self.setUpClass()
        redis_check = roesifier.check_redis_connection(self.redis_connection)
        self.assertTrue(redis_check)


if __name__ == '__main__':
    unittest.main()
