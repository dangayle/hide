Hide
============

A steganography python script for encrypting/hiding a zipfile within a image file. Uses [bcrypt](https://github.com/pyca/bcrypt/) for the password key deriviation function and [PyNaCl](https://github.com/pyca/pynacl) for the secret-key cryptography.

###How to hide a file
To hide and encrypt a zipfile:

```
python hide.py -i batman.gif -a zip_archive.zip
```

You'll be asked for a password and then you're done. If it blows up, it didn't work.

###How to unhide a file
To unhide and decrypt a zipfile:

```
python hide.py -u batman.gif -d
```
Optional `-d` flag decompresses the archive to same dir as the image file.

###Caveats
I didn't attempt to invent my own cryptography, so Hide is built using the excellent and cryptographically sound [bcrypt](https://github.com/pyca/bcrypt/) and [PyNaCl](https://github.com/pyca/pynacl) libraries. Don't roll your own crypto.

The actual [steganography](http://en.wikipedia.org/wiki/Steganography) part of this script is painfully awkward, not like the "least significant bit" kinds of steganography. Although the crypto is secure, the hidden archive file is easily detectable by someone with decent CS knowledge, meaning although they can't open the file, they might know it exists.


###Tests
Tests pass `python -m unittest tests.test_hide`

###Requirements
Requires [bcrypt](https://github.com/pyca/bcrypt/) and [PyNaCl](https://github.com/pyca/pynacl), which you can `pip` install.

###License
Uses the [MIT license](https://github.com/dangayle/hide/blob/master/LICENSE)

###TODO
* Find a better way to write the data to the image. I think doing bytecounts and using those as a flag at the end of the file would be a more robust way to do it, but I'm not 100% certain. Something like `image.write(encrypted_file + salt + len(encrypted_file) + len(salt))`, but then I don't know how many bytes to count when decrypting it.
* Maybe add the zip compression directly into the script?
* Make the filepaths more flexible
* Make a copy of the original image rather than editing in place?
