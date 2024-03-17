import unittest

from smartrewind.video import upload

class TestUpload(unittest.TestCase):
    def test_upload(self): #Tested, returning now to prevent unnecessary uploads
        return
        filename = "C:/Users/Mohammad Saif/Documents/Masters/MSc Project/code/smartrewind/assets/testfile.txt"
        success = upload(filename)
        self.assertEqual(success, True, "Failure is not an option")

    def test_filename_none(self):
        with self.assertRaises(Exception):
            upload(file_name=None)

    def test_wrong_filename(self):
        with self.assertRaises(Exception):
            upload(file_name="C:/Users/Mohammad Saif/Documents/Masters/MSc Project/code/assets/testfile.txt")

if __name__ == '__main__':
    unittest.main()