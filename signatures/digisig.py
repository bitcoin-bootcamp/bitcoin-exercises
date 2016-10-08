#!/usr/bin/env python
import click
import ecdsa
import hashlib
import random

def create_keys(secret):
    """Create the ECDSA key pair"""
    # Enter a random private key from https://bitcore.io/playground/#/address
    pk = secret.decode('hex')

    # Generate a 512-bit public key from the private key (pk) using ECDSA
    sk = ecdsa.SigningKey.from_string(pk, curve=ecdsa.SECP256k1)

    # Write the private key to disk
    open("sk.pem","w").write(sk.to_pem())

    # Write the public key to disk
    vk = sk.verifying_key
    open("vk.pem","w").write(vk.to_pem())

    return (sk, vk)

@click.group()
def digisig():
    pass

@digisig.command()
@click.option('--message', '-m', prompt='Your message', help='The message to sign')
@click.option('--secret', '-s', prompt='Your private (secret) key', help='Private key (in hex)')
def sign(message, secret):
    """
    Sign a message using a private key
    """
    # Create the public key
    sk, vk = create_keys(secret)

    # In Bitcoin much more occurs here
    m = message

    # Create the signature
    sig = sk.sign(m, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)

    # Write the message to disk for later
    open("msg.txt","w").write(m)

    # Write the signature to disk for later
    open("sig.der","w").write(sig)

    click.echo(click.style('Message signed!', fg='yellow'))
    click.echo(click.style('Wrote 4 files (msg.txt, sk.pem, vk.pem, sig.der)', fg='magenta'))

    click.echo(click.style('Note: ', fg='white', bold=True) + 'You can use OpenSSL to verify the signature!')
    click.echo('Simply run: openssl dgst -sha256 -verify vk.pem -signature sig.der msg.txt')

    return

@digisig.command()
@click.argument('signature', type=click.Path(exists=True))
@click.argument('message', type=click.Path(exists=True))
@click.argument('public_key', type=click.Path(exists=True))
def verify(signature, message, public_key):
    """
    Verify a message given the signature, message, and public key files
    """
    sig = open(signature, "r").read()
    msg = open(message,"r").read()
    vk = ecdsa.VerifyingKey.from_pem(open(public_key,"r").read())
    try:
        is_valid = vk.verify(sig, msg, hashfunc=hashlib.sha256, sigdecode=ecdsa.util.sigdecode_der)
    except:
        is_valid = False
    
    prefix = click.style('Signature: ', fg='white', bold=True)
    if is_valid:
        click.echo(prefix + click.style('Valid!', fg='green'))
    else:
        click.echo(prefix + click.style('Invalid :(', fg='red'))

    return

if __name__ == '__main__':
    digisig()
