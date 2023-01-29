import final.fastapi_server.fastapifunc as fastapifunc
import unittest


class TestFastApi(unittest.TestCase):

    def setUp(self):
        return True

    @classmethod
    def setUpClass(cls):
        test_file1_contents = b"this is "
        file2_contents = b"a test "
        with open('example_a.txt', "wb") as file1:
            file1.write(test_file1_contents)
        with open('example_b.txt', "wb") as file2:
            file2.write(file2_contents)
        read_file1 = open('example_a.txt', "rb").read()
        read_file2 = open('example_b.txt', "rb").read()
        return read_file1, read_file2

    def test_encrypt_func(self):
        read_file1 = self.setUpClass()[0]
        read_file2 = self.setUpClass()[1]
        full_file = read_file1 + read_file2
        full_func = fastapifunc.encrypt(read_file1, read_file2)
        file_with_hash = full_func[0]
        only_hash = full_func[1]
        test = full_file + only_hash
        self.assertEqual(test, file_with_hash)


    def check_files_append(self):
        file1 = open("example_a.txt", "w").write("this is")
        file2 = open("example_b.txt", "w").write("a test")
        roesifier.process_new_file(file1)
        roesifier.process_new_file(file2)


if __name__ == '__main__':
    unittest.main()
