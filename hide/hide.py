"""
Encrypt and hide a zipfile in an image or unpack an image with a hidden
archive in it.
"""

import os
import sys
import argparse
import StringIO
import warnings
from getpass import getpass
from zipfile import ZipFile, BadZipfile
from bcrypt import gensalt, hashpw

with warnings.catch_warnings():
    """Suppress this warning (for now?):
    /usr/local/lib/python2.7/site-packages/cffi/vengine_cpy.py:166:
        UserWarning: reimporting '_cffi__x332a1fa9xefb54d7c'
        might overwrite older definitions % (self.verifier.get_module_name()))
    """
    warnings.simplefilter("ignore")
    import nacl.utils
    from nacl.secret import SecretBox
    from nacl.exceptions import CryptoError

def key_32(salt):
    """Returns 32 byte key"""
    return hashpw(getpass(), salt)[-32:]


def hide(image_file, archive_file):
    """Append an encrypted archive onto the end of an image"""

    salt = gensalt()
    box = SecretBox(key_32(salt))
    nonce = "dg1" + nacl.utils.random(21)

    with open(image_file, "ab") as image:
        with open(archive_file, "rb") as a:
            archive = a.read()
            # Append the encrypted contents of the archive onto the image, along with the salt
            image.write("EOF" + box.encrypt(archive, nonce) + "EOF" + salt)


def unhide(unhide_file, decompress=False):
    """Unhide and decompress hidden zipfile"""

    unhide_path = os.path.dirname(unhide_file)

    with open(unhide_file, "rb") as f:
        hidden_file = f.read()

        try:
            image, encrypted_zip, salt = hidden_file.split("EOF")
        except ValueError:
            print("No archive found in image.")
            sys.exit(1)

        box = SecretBox(key_32(salt))

        try:
            decrypted_zip = box.decrypt(encrypted_zip)
        except CryptoError:
            print("Unhide failed. Wrong password.")
            sys.exit(1)

        # zipfile needs a file-like object
        e_string = StringIO.StringIO()
        e_string.write(decrypted_zip)

        if decompress:
            with ZipFile(e_string) as zipfile:
                try:
                    zipfile.extractall(unhide_path)
                except BadZipfile:
                    print("Could not decompress file. Bad zipfile.")
                    sys.exit(1)
        else:
            with open(os.path.join(unhide_path, "archive.zip"), "w") as zipfile:
                zipfile.write(decrypted_zip)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
    hide = parser.add_argument_group('Hide', hide.__doc__)
    hide.add_argument('-i', '--image_file', default=None,
        help="Image to hide archive in")
    hide.add_argument('-a', '--archive_file', default=None,
        help="Archive to be hidden")
    unhide = parser.add_argument_group('Unhide', unhide.__doc__)
    unhide.add_argument('-u', '--unhide', default=None,
        help="Filename of image with hidden archive to be extracted")
    unhide.add_argument('-d', '--decompress', default=False, action="store_true",
        help="Decompress file to same location as image")
    args = parser.parse_args()
    if args.image_file and args.archive_file:
        hide(args.image_file,args.archive_file)
    if args.unhide:
        unhide(args.unhide, args.decompress)
