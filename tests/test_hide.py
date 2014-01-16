import unittest
import warnings
import tempfile
import os
import hide.hide as hide

# Usage:
# python -m unittest tests.test_hide


def fake_getpass(*args):
    return "test"


def cleanup_getpass(module, old_getpass):
    module.getpass = old_getpass


class test_hide(unittest.TestCase):

    def setUp(self):
        self.old_getpass = hide.getpass
        hide.getpass = fake_getpass
        self.salt = hide.gensalt()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            self.temp_file = f
            f.write("bojangles")

    def tearDown(self):
        cleanup_getpass(hide, self.old_getpass)
        os.unlink(self.temp_file.name)

    def test_key_32(self):
        salt = self.salt
        key = hide.key_32(salt)
        self.assertEqual(len(key), 32)

    def test_hide(self):
        # hide.hide(self.temp_file, )
        # with open(self.temp_file.name) as f:
        #     content = f.read()
        #     print content
        pass

    def test_unhide(self):
        # print self.temp_file.name
        pass


# with tempfile.NamedTemporaryFile(delete=False) as f:
#     f.write("hi dan")

# with open(f.name) as f:
#     contents = f.read()
