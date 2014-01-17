import unittest
import warnings
import tempfile
import os
import sys
import shutil
import zipfile
import hide.hide as hide
import pdb


# Usage:
# python -m unittest tests.test_hide


def mock_getpass(*args):
    return "test"


def mock_gensalt(*args):
    return "$2a$12$kHWRtLWiIl1nzITDkWkDbO"


def cleanup_getpass(module, old_getpass):
    module.getpass = old_getpass


def cleanup_gensalt(module, old_gensalt):
    module.gensalt = old_gensalt


class test_hide(unittest.TestCase):

    def setUp(self):
        '''Create tempfiles to work with, and mock the pass and salt'''

        self.old_getpass = hide.getpass
        hide.getpass = mock_getpass
        self.old_gensalt = hide.gensalt
        hide.gensalt = mock_gensalt
        self.salt = hide.gensalt()
        tempfile.tempdir = None
        tempfile.tempdir = tempfile.mkdtemp()

        # Need a temp file to hide stuff in
        with tempfile.NamedTemporaryFile(delete=False) as f:
            self.temp_file = f
            f.write("bojangles")

        # Need a temp zipfile encrypt
        with tempfile.NamedTemporaryFile(delete=False) as z:
            self.temp_zip = z
            temp_zip = zipfile.ZipFile(z.name, 'w')
            temp_zip.writestr("bogart.txt", "bogart")
            temp_zip.close()

    def tearDown(self):
        '''Restore original modules and clean up temp files'''
        cleanup_getpass(hide, self.old_getpass)
        cleanup_gensalt(hide, self.old_gensalt)
        os.unlink(self.temp_file.name)
        os.unlink(self.temp_zip.name)
        shutil.rmtree(tempfile.gettempdir())

    def test_key_32(self):
        key = hide.key_32(self.salt)
        self.assertEqual(len(key), 32)
        self.assertEqual(key, "OTePKw6L1d6IpIPfe/iJiaRYeHMUP6wO")

    def test_hide(self):
        '''Encrypt temp zipfile'''
        # pass
        hide.hide(self.temp_file.name, self.temp_zip.name)
        self.assertEqual(os.path.getsize(self.temp_file.name), 208)

    def test_unhide(self):
        '''Encrypt then unencrypt an archive file'''
        hide.hide(self.temp_file.name, self.temp_zip.name)
        hide.unhide(self.temp_file.name)
        with self.assertRaises(ValueError):
            hide.unhide(self.temp_zip.name)
        self.assertTrue(os.path.isfile(os.path.join(tempfile.gettempdir(), "bogart.txt")))
