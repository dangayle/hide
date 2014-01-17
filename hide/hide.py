'''Encrypt and hide a zipfile in an image or unpack an image with a hidden archive in it'''

import os
import sys
import argparse
import StringIO
import warnings
from getpass import getpass
from zipfile import ZipFile
from bcrypt import gensalt, hashpw

with warnings.catch_warnings():
    '''Suppress this warning (for now?):
    /usr/local/lib/python2.7/site-packages/cffi/vengine_cpy.py:166: UserWarning: reimporting '_cffi__x332a1fa9xefb54d7c' might overwrite older definitions
  % (self.verifier.get_module_name()))
    '''
    warnings.simplefilter("ignore")
    import nacl.utils
    from nacl.secret import SecretBox


def key_32(salt):
    '''Returns 32 byte key'''
    return hashpw(getpass(), salt)[-32:]


def hide(image_file, archive_file):
    '''Append an encrypted archive onto the end of an image'''

    salt = gensalt()
    box = SecretBox(key_32(salt))
    nonce = "dg1" + nacl.utils.random(21)

    # open the image file in "append binary" mode
    with open(image_file, "ab") as image:
        # open the archive file in "read only binary" mode
        with open(archive_file, "rb") as a:
            archive = a.read()
            # Append the encrypted contents of the archive onto the image, along with the salt
            image.write("EOF" + box.encrypt(archive, nonce) + "EOF" + salt)


def unhide(unhide_file):
    '''Unpack a zipfile'''

    with open(unhide_file, "rb") as f:
        hidden_file = f.read()
        # split file into component parts
        image, encrypted, salt = hidden_file.split("EOF")
        box = SecretBox(key_32(salt))
        try:
            decrypted = box.decrypt(encrypted)
        except:
            raise
        # zipfile needs a file-like object
        e_string = StringIO.StringIO()
        e_string.write(decrypted)
        archive = ZipFile(e_string)
        try:
            # sys.stdout.write("\n\nExtracting files:\n")
            # print os.path.dirname(unhide_file)
            # archive.printdir()
            archive.extractall(os.path.dirname(unhide_file))
            # sys.stdout.write("Files sucessfully extracted\n\n")
        except:
            raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hide', nargs=2)
    parser.add_argument('-U', '--unhide')
    args = parser.parse_args()
    if args.hide:
        hide(*args.hide)
    if args.unhide:
        unhide(args.unhide)
