#!/usr/bin/env python
import click
import hashlib
from treelib import Node, Tree

merkle_tree = Tree()
merkle_tree.create_node('root', 'root')

def merkle(hashList):
    """
    Calculate the Merkle Root recursively
    """

    # If a single name then return the hash
    if len(hashList) == 1:
        return hashList[0]

    newHashList = []
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList)-1, 2):
        new_node = hash2(hashList[i], hashList[i+1])
        newHashList.append(new_node)

    # If odd, hash last item twice
    if len(hashList) % 2 == 1:
        odd_node = hash2(hashList[-1], hashList[-1])
        newHashList.append(odd_node)

    return merkle(newHashList)

def hash2(a, b):
    """
    Hash nodes A and B
    """
    a1 = a.decode('hex')
    b1 = b.decode('hex')
    h = hashlib.sha256(a1+b1).digest().encode('hex')

    # Build the merkle tree
    merkle_tree.create_node(disp_hash(h), h, parent='root')
    if merkle_tree.contains(a): merkle_tree.move_node(a, h)
    if merkle_tree.contains(b): merkle_tree.move_node(b, h)

    return h

def hash_leaf(node):
    """
    Hash the leaf nodes
    """
    hash_value = hashlib.sha256(node).digest().encode('hex')
    merkle_tree.create_node(disp_hash(hash_value), hash_value, parent='root')
    return hash_value

def disp_hash(hash_value):
    """
    Pretty print the hash value
    """
    return hash_value[0:3] + '...' + hash_value[-3::1]

@click.command()
@click.argument('names', nargs=-1)
def make_tree(names):
    """
    Build the Merkle Tree
    """
    # Start by hashing the leaves
    hashed_leaves = list(map(hash_leaf, names))

    # Print out the number of leaves
    numLeaves = len(hashed_leaves)
    click.echo(click.style('Number of leaves: ', fg='yellow') + '%i' % numLeaves)

    # Calculate the merkle root
    merkleroot = merkle(hashed_leaves)
    click.echo(click.style('Merkle root: ', fg='yellow') + merkleroot)

    # Display the merkle tree
    click.echo(click.style('Merkle tree: ', fg='yellow'))
    merkle_tree.root = merkleroot
    merkle_tree.show(line_type="ascii-em")

    return

if __name__ == '__main__':
    make_tree()
