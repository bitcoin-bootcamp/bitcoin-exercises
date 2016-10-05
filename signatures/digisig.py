#!/usr/bin/env python
import click
import ecdsa
import hashlib
import random

def write_keys(secret):
    """Create the ECDSA key pair"""
    # Enter a random private key from https://bitcore.io/playground/#/address
    pk = secret.decode('hex')

    # Generate a 512-bit public key from the private key (pk) using ECDSA
    sk = ecdsa.SigningKey.from_string(pk, curve=ecdsa.SECP256k1)

    # Write the private key to disk
    open("priv.pem","w").write(sk.to_pem())

    # Write the public key to disk
    vk = sk.verifying_key
    open("pub.pem","w").write(vk.to_pem())

    return (sk, vk)

@click.group()
def digisig():
    pass

@digisig.command()
@click.option('--message', '-m', default='Hello world', prompt='Your message', help='The message to sign')
@click.option('--secret', '-s', prompt='Your private key', help='Private key in hex')
def sign(message, secret):
    """Sign a message using a private key"""
    sk, vk = write_keys(secret)
    m = message
    sig = sk.sign(m, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)

    # Write the signature to disk
    open("sig.der","w").write(sig)

    click.echo(click.style('Message: ', fg='yellow') + '%s' % m)
    click.echo(click.style('Signature: ', fg='yellow') + '%s' % sig.encode('Base64'))
    click.echo(click.style('Wrote 3 files (priv.pem, pub.pem, sig.der)', fg='magenta'))

    # Write the message to disk
    open("message.txt","w").write(m)

    click.echo(click.style('Note: ', fg='white', bold=True) + 'You can use OpenSSL to verify the signature.')
    click.echo('Simply run: openssl dgst -sha256 -verify pub.pem -signature sig.der message.txt')

    return

@digisig.command()
@click.option('--signature', '-sig', prompt='The digital signature', help='The digital signature of a message')
@click.option('--message', '-m', default='Hello world', prompt='Your message', help='The message to sign')
@click.option('--publickey', '-p', prompt='The public key associated with the signature', help='The public key associated with the signature')
def verify(signature, message, publickey):
    """Verify a message given a signature and public key"""

    # Convert publickey into vk (vk.from_pem())
    
    # print vk.verify(sig, m)
    click.echo(click.style('This is an output: ', fg='yellow') + 'This is normal')

    return

if __name__ == '__main__':
    digisig()
