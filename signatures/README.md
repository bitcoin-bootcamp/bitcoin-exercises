# Digital Signatures

The easiest way to play with digital signatures is to use the pybitcointools library!

You can get a feel for digital signatures by going through this exercise:
```
$ git clone https://github.com/vbuterin/pybitcointools.git
$ cd pybitcointools
$ python
>>> from bitcoin import *
>>> sk = random_key()  # Generate a private key
>>> vk = privtopub(sk) # Generate a public key
>>> msg = 'hello world' # Create a simple message
>>> sig = ecdsa_sign(msg, sk) # Sign the message using your private key
>>> print sig
GxXGAt...2L/eJk=
>>> print ecdsa_verify(msg, sig, vk) # Use sig and public key to verify
True
>>> msg = 'hello mars' # Change the message
>>> print ecdsa_verify(msg, sig, vk) # Changing the msg invalidates sig
False
```

You can also take a look at the `digisig.py` tool in the `signatures` folder which uses the python ecdsa library. It will generate files so that OpenSSL can be used to verify the signature.

Here's how to use the digisig tool:

```
$ python digisig.py sign --message 'hello world' --secret 'e1e78ca3ebbce24977ddd8161905e7ee6821c0a100a6c1a58ac2e0cf79f98635'
Message signed!
Wrote 4 files (msg.txt, sk.pem, vk.pem, sig.der)
Note: You can use OpenSSL to verify the signature!
Simply run: openssl dgst -sha256 -verify vk.pem -signature sig.der msg.txt
```

To verify:
```
$ python digisig.py verify sig.der msg.txt vk.pem
Signature: Valid!
```

Or verify using OpenSSL by passing in the public key, signature and message respectively:
```
$ openssl dgst -sha256 -verify vk.pem -signature sig.der msg.txt
Verified OK
```
