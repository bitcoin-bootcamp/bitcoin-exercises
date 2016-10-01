#!/usr/bin/python
""" Generate a 2 of 3 multisignature address

"""

import click

from bitcoin import *

class MultiSignature(object):

    def generate_address(self):

        private_key_one = self.generate_private_key()
        private_key_two = self.generate_private_key()
        private_key_three = self.generate_private_key()

        public_key_one = self.get_public_key(private_key_one)
        public_key_two = self.get_public_key(private_key_two)
        public_key_three = self.get_public_key(private_key_three)

        print "Generated private keys:"
        print "One - ", self.get_public_address(public_key_one)
        print "Two - ", self.get_public_address(public_key_two)
        print "Three - ", self.get_public_address(public_key_three)

        redeem_script = self.create_redeem_script([public_key_one, public_key_two, public_key_three])

        print "Redeem script:"
        print redeem_script

        multisignature_address = self.redeem_script_to_address(redeem_script)

        print "Multisignature address:"
        print multisignature_address

    @staticmethod
    def generate_private_key():
        return sha256(str(random.randrange(2**256)))

    # Function aliases - modified for readability
    @staticmethod
    def get_public_key(private_key):
        return privtopub(private_key)

    @staticmethod
    def get_public_address(public_key):
        return pubtoaddr(public_key)

    @staticmethod
    def create_redeem_script(public_keys):
        return mk_multisig_script(public_keys, 2, 3)

    @staticmethod
    def redeem_script_to_address(redeem_script):
        return p2sh_scriptaddr(redeem_script)

@click.group(help='')
def cli():
    pass

@click.command('generate_address')
def generate_address():
    MultiSignature().generate_address()

cli.add_command(generate_address)

if __name__ == '__main__':
    cli()

