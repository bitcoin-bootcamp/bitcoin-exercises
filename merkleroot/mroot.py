#!/usr/bin/env python
import click
import hashlib
import json

# Hash pairs of items recursively until a single value is obtained
def merkle(hashList):
    """Comments"""
    # If a single transaction then return the transaction hash
    if len(hashList) == 1:
        return hashList[0]

    newHashList = []

    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList)-1, 2):
        newHashList.append(hash2(hashList[i], hashList[i+1]))

    if len(hashList) % 2 == 1: # odd, hash last item twice
        newHashList.append(hash2(hashList[-1], hashList[-1]))

    return merkle(newHashList)

def hash2(a, b):
    """
    # Reverse inputs before and after hashing
    # due to big-endian / little-endian nonsense
    """
    a1 = a.decode('hex')[::-1]
    b1 = b.decode('hex')[::-1]
    h = hashlib.sha256(hashlib.sha256(a1+b1).digest()).digest()
    return h[::-1].encode('hex')

@click.command()
@click.argument('f', type=click.Path(exists=True))
def mroot(f):
    """Comments"""
    filename = open(f, 'r')
    block = json.loads(filename.read())

    # Print out the number of transactions in the block
    numTxs = len(block["transaction_hashes"])
    click.echo(click.style('Number of transactions: ', fg='yellow') + '%i' % numTxs)

    # Print out the merkle root of the block
    mrt = block["merkle_root"]
    click.echo(click.style('Merkle root in block header: ', fg='yellow') + mrt)

    # Calculate the merkle root
    merkleroot = merkle(block["transaction_hashes"])
    click.echo(click.style('Merkle root of transactions: ', fg='yellow') + merkleroot)

    # Print out whether calculated merkle root matches the Merkle Root in the block
    if (merkleroot == block["merkle_root"]):
        click.echo(click.style('Valid Merkle Root!', fg='green'))
    else:
        click.echo(click.style('Something went wrong :(', fg='red'))

    return

if __name__ == '__main__':
    mroot()
