#!/usr/bin/python
""" A library designed for demonstration of simple wallet functionality

"""

import click, requests

from bitcoin import *
from termcolor import colored
from tabulate import tabulate

class Wallet(object):


    def generate_address(self, testnet):

        private_key = self.generate_private_key()

        print colored("Generate private key:", "yellow")
        print "\t", private_key

        public_key = self.get_public_key(private_key)

        print colored("Generated public key:", "yellow")
        if testnet:
            print "\t", self.get_public_address_testnet(public_key)
        else:
            print "\t", self.get_public_address(public_key)


    def generate_multisig_address(self, testnet):

        private_key_one = self.generate_private_key()
        private_key_two = self.generate_private_key()
        private_key_three = self.generate_private_key()

        print colored("Generate private keys:", "yellow")
        print "\t1 - ", private_key_one
        print "\t2 - ", private_key_two
        print "\t3 - ", private_key_three        

        public_key_one = self.get_public_key(private_key_one)
        public_key_two = self.get_public_key(private_key_two)
        public_key_three = self.get_public_key(private_key_three)

        print colored("Generated public keys:", "yellow")
        if testnet:
            print "\t1 - ", self.get_public_address_testnet(public_key_one)
            print "\t2 - ", self.get_public_address_testnet(public_key_two)
            print "\t3 - ", self.get_public_address_testnet(public_key_three)
        else:
            print "\t1 - ", self.get_public_address(public_key_one)
            print "\t2 - ", self.get_public_address(public_key_two)
            print "\t3 - ", self.get_public_address(public_key_three)

        redeem_script = self.create_redeem_script([public_key_one, public_key_two, public_key_three])

        print colored("Redeem script:", "yellow")
        print "\t", redeem_script

        if testnet:
            multisignature_address = self.redeem_script_to_address_testnet(redeem_script)
        else:
            multisignature_address = self.redeem_script_to_address(redeem_script)

        print colored("Multisignature address:", "yellow")
        print "\t", multisignature_address


    def get_unspents(self, address, testnet, json):

        table = []

        # Make a request to the BitGo API to retrieve all unspent Bitcoin associated
        # with the provided address
        if testnet:
            response = requests.get('https://test.bitgo.com/api/v1/address/' + address + '/tx')
        else:
            response = requests.get('https://www.bitgo.com/api/v1/address/' + address + '/tx')
            
        try:
            transactions = response.json()['transactions']
        except:
            print 'No unspents found for address: ', address
            return

        utxos = []

        # Retrieve the necessary information from the transaction payload
        for transaction in transactions:
          date = transaction['date']
          unspents = transaction['outputs']
          transaction_id = transaction['id']
          for unspent in unspents:
              if unspent['account'] == address:
                utxos.append({'output': transaction_id + ':' + str(unspent['vout']), 'value': unspent['value']})
                table.append([date, transaction_id, unspent['account'], unspent['value'], unspent['vout']])

        if json:
            print colored("Unspent Transactions", "yellow")
            print "\t Address: ", address
            print "\t", utxos
            return utxos

        print tabulate(table, headers=["Date", "Transaction ID", "Address", "Value", "Vout"])


    def create_raw_transaction(self, address, amount, testnet):
        outputs = self.get_unspents(address, testnet, json=True)
        raw_transaction =  self._create_raw_transaction(outputs, address, amount)
        print colored("Raw unsigned transaction:", "yellow")
        print "\t", raw_transaction


    def create_and_sign_raw_transaction(self, address, amount, private_key, testnet):
        outputs = self.get_unspents(address, testnet, json=True)
        raw_transaction =  self._create_raw_transaction(outputs, address, amount)

        print colored("Raw unsigned transaction:", "yellow")
        print "\t", raw_transaction 
        utxos = []
        for utxo in outputs:
            utxos.append({utxo['output']: private_key})

        raw_signed_transaction = sign(raw_transaction, 0, private_key)
        print colored("Raw signed transaction:", "yellow")
        print raw_signed_transaction


    def sign_transaction(self, private_key, transaction):
        index = 0
        signed_transaction = self._sign_transaction(transaction, index, private_key)
        print colored("Signed transaction:", "yellow")
        print signed_transaction


    def sign_multisignature_transaction(self, private_key, script, transaction):
        index = 0
        signed_transaction = self._sign_multisignature_transaction(transaction, index, script, private_key)
        print colored("Signed multisignature unspent:", "yellow")
        print signed_transaction


    # Address creation methods

    @staticmethod
    def generate_private_key():
        return sha256(str(random.randrange(2**256)))


    @staticmethod
    def get_public_key(private_key):
        return privtopub(private_key)


    @staticmethod
    def get_public_address(public_key):
        return pubtoaddr(public_key)


    @staticmethod
    def get_public_address_testnet(public_key, magicbytes=111):
        return pubtoaddr(public_key, magicbytes)


    @staticmethod
    def create_redeem_script(public_keys):
        return mk_multisig_script(public_keys, 2, 3)


    @staticmethod
    def redeem_script_to_address_testnet(redeem_script):
        return p2sh_scriptaddr(redeem_script, 0xc4)


    @staticmethod
    def redeem_script_to_address(redeem_script):
        return p2sh_scriptaddr(redeem_script)

    # Transaction creation and signing methods

    @staticmethod
    def _create_raw_transaction(outputs, address, amount):
        ins = outputs
        outs = [{'value': int(amount), 'address': address}]
        return mksend(ins, outs, address, 1000000)


    @staticmethod
    def _sign_transaction(transaction, index, private_key):
        return sign(str(transaction), int(index), private_key)

    @staticmethod
    def _sign_multisignature_transaction(transaction, index, script, private_key):
        return multisign(transaction, index, script, private_key)



@click.group(help='')
def cli():
    pass

@click.command('generate_address')
@click.option('--testnet', help='Testnet flag', is_flag=True)
def generate_address(testnet):
    Wallet().generate_address(testnet)


@click.command('generate_multisig_address')
@click.option('--testnet', help='Testnet flag', is_flag=True)
def generate_multisig_address(testnet):
    Wallet().generate_multisig_address(testnet)


@click.command('get_unspents')
@click.option('--address', help='Bitcoin address', required=True)
@click.option('--testnet', help='Testnet flag', is_flag=True)
@click.option('--json', help='Return JSON', is_flag=True)
def get_unspents(address, testnet, json):
    Wallet().get_unspents(address, testnet, json)


@click.command('create_raw_transaction')
@click.option('--address', help='The recipients address', required=True)
@click.option('--amount', help='The amount to send', required=True)
@click.option('--testnet', help='Testnet flag', is_flag=True)
def create_raw_transaction(address, amount, testnet):
    Wallet().create_raw_transaction(address, amount, testnet)


@click.command('create_and_sign_raw_transaction')
@click.option('--address', help='The recipients address', required=True)
@click.option('--private_key', help='The private key associated with the unspent', required=True)
@click.option('--amount', help='The amount to send', required=True)
@click.option('--testnet', help='Testnet flag', is_flag=True)
def create_and_sign_raw_transaction(address, amount, private_key, testnet):
    Wallet().create_and_sign_raw_transaction(address, amount, private_key, testnet)


@click.command('sign_transaction')
@click.option('--private_key', help='Private key', required=True)
@click.option('--transaction', help='Transaction', required=True)
def sign_transaction(private_key, transaction):
    Wallet().sign_transaction(private_key, transaction)


@click.command('sign_multisignature_transaction')
@click.option('--private_key', help='Private key', required=True)
@click.option('--transaction', help='The raw transaction', required=True)
@click.option('--script', help='The redeem script', required=True)
def sign_multisignature_transaction(private_key, transaction, script):
    Wallet().sign_multisignature_transaction(private_key, transaction, script)


cli.add_command(generate_multisig_address)
cli.add_command(generate_address)
cli.add_command(get_unspents)
cli.add_command(create_raw_transaction)
cli.add_command(create_and_sign_raw_transaction)
cli.add_command(sign_transaction)


if __name__ == '__main__':
    cli()

