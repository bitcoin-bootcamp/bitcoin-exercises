#!/usr/bin/python
""" A bip32 library designed for demonstration of hierarchical deterministic wallet concepts

"""

import click

from bitcoin import *
from termcolor import colored


class HdWallet(object):

    def generate_address(self):

        bip_32_seed = 'MASTER_SEED'
        master_private_key = bip32_master_key(bip_32_seed)
        master_public_key = bip32_privtopub(master_private_key)

        print colored("Master private key:", "yellow")
        print master_private_key
        print colored("Master public key:", "yellow")
        print master_public_key

        level_one_private_zero = bip32_ckd(master_private_key, 0)
        level_one_public_zero = bip32_privtopub(level_one_private_zero)

        print colored("Level 1, index 0 - private key:", "yellow")
        print level_one_private_zero
        print colored("Level 1, index 0 - public key", "yellow")
        print level_one_public_zero

        level_two_private_zero = bip32_ckd(level_one_private_zero, 0)
        level_two_public_zero = bip32_privtopub(level_two_private_zero)

        print colored("Level 2, index 0 - private key:", "yellow")
        print level_two_private_zero
        print colored("Level 3, index 0 - public key", "yellow")
        print level_two_public_zero

        level_three_private_zero = bip32_ckd(level_two_private_zero, 0)
        level_three_public_zero = bip32_privtopub(level_three_private_zero)

        print colored("Level 3, index 0 - private key:", "yellow")
        print level_three_private_zero
        print colored("Level 3, index 0 - public key", "yellow")
        print level_three_public_zero

        level_four_private_zero = bip32_ckd(level_three_private_zero, 0)
        level_four_public_zero = bip32_privtopub(level_four_private_zero)
        print colored("Level 4, index 0 - private key:", "yellow")
        print level_four_private_zero
        print colored("Level 4, index 0 - public key", "yellow")
        print level_four_public_zero


@click.group(help='')
def cli():
    pass


@click.command('generate_address')
def generate_address():
    HdWallet().generate_address()


cli.add_command(generate_address)


if __name__ == '__main__':
    cli()

