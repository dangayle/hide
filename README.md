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
Everyone tells us to absolutely **DO  NOT** try to invent our own cryptography schemes, so I've tried to follow the best practices for the encryption part of this, following the suggestions from the fine folks on Twitter and the ```#python``` IRC, but I'm not a security expert.

###Requirements

Requires [bcrypt](https://github.com/pyca/bcrypt/) and [PyNaCl](https://github.com/pyca/pynacl), which you can `pip` install.

###License
Uses the [MIT license](https://github.com/dangayle/hide/blob/master/LICENSE)
