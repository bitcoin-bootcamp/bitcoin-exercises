# Merkle Tree

## Simple Example
To see how a merkle tree works at a high-level, you can play with the `merkle_tree.py` tool:
```
$ python merkle_tree.py 'Alexandra' 'Alex'
Number of leaves: 2
Merkle root: 4b9ff184f02d0e048f4c71ac28a90806749742e9b90e3ff8c000ddfecc044f82
Merkle tree:
4b9...f82
╠══ 9cb...817
╚══ db7...97a
```

If you add more names to the tree, you'll notice that the merkle tree with root `4b9...f82` becomes a sub tree:
```
$ python merkle_tree.py 'Alexandra' 'Alex' 'Mike' 'Mark' 'Otto'
Number of leaves: 5
Merkle root: a693f2f239955618acb8544326ea1b96edd8a8d69d152b8213b57aafa6f677f8
Merkle tree:
a69...7f8
╠══ e5f...1db
║   ╚══ 973...2e1
║       ╚══ d7c...e21
╚══ f64...9d3
    ╠══ 4b9...f82
    ║   ╠══ 9cb...817
    ║   ╚══ db7...97a
    ╚══ d00...562
        ╠══ 9dc...3f7
        ╚══ d7c...2bc
```

## Bitcoin Example
To see how merkle roots are calculated in Bitcoin, you can peer into `mroot.py`. Currently it is pulling from toshi.io which is offline at the moment. However it still returns data for older blocks. Some blocks worth testing:

* Block 0 - The Genesis Block - 1 transaction
* Block 170 - 2 transactions
* Block 546 - 3 transactions
* Block 586 - 4 transactions
* Block 150,000 - 10 transactions

Just pass it the height of the block:
```
$ python mroot.py 0
Number of transactions: 1
Merkle root in block header: 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b
Merkle root of transactions: 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b
Valid Merkle Root!
```
