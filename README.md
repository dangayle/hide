Hide
============

A steganography python script for encrypting/hiding a zipfile within a image file. Uses [bcrypt](https://github.com/pyca/bcrypt/) for the password key deriviation function and [PyNaCl](https://github.com/pyca/pynacl) for the secret-key cryptography.

###How to hide a file
To hide and encrypt a zipfile, use the `-H` argument and feed it the name of the image and the name of the archive:

```python
python hide.py -H batman.gif zip_archive.zip
```

You'll be asked for a password and then you're done. If it blows up, well, it didn't work.

###How to unhide a file
To unhide and decrypt a zipfile, use the `-U` argument and feed it the name of the image containing the encrypted archive

```python
python hide.py -U batman.gif
```

###Caveats
The actual [steganography](http://en.wikipedia.org/wiki/Steganography) part of this script is painfully trivial, not like the "least significant bit" kind of hiding stuff, so your mileage may vary.

Everyone tells us to absolutely **DO  NOT** try to invent our own cryptography schemes, so I've tried to follow the best practices for the encryption part of this, following the suggestions from the fine folks on Twitter and the ```#python``` IRC, but I'm not a security expert. I'm going to get people smarter than me to look at it.

###Tests
I think I about covered it with the tests. They all pass, so whoop!

###Requirements
Requires [bcrypt](https://github.com/pyca/bcrypt/) and [PyNaCl](https://github.com/pyca/pynacl), which you can `pip` install.

###License
Uses the [MIT license](https://github.com/dangayle/hide/blob/master/LICENSE)

###TODO
* Find a better way to write the data to the image. I think doing bytecounts and using those as a flag at the end of the file would be a more robust way to do it, but I'm not 100% certain. Something like `image.write(encrypted_file + salt + len(encrypted_file) + len(salt))`, but then I don't know how many bytes to count when decrypting it.
* Maybe add the zip compression directly into the script?
* Make the filepaths more flexible
* Make a copy of the original image rather than editing in place?
