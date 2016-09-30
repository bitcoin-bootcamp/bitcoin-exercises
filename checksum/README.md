# Checksum

**Play-by-play:** [CLI Demo](http://showterm.io/d00ae10bb8c6a0175ead5)

## Step 1
In the `checksum` directory, you’ll see 3 files containing the following quotes:

**quote1.txt**
```
The Times 03/Jan/2009 Chancellor on brink of second bailout for banks
```

**quote2.txt**
```
It might make sense just to get some in case it catches on. If enough people think the same way, that becomes a self fulfilling prophecy.
```

**quote3.txt**
```
Commerce on the Internet has come to rely almost exclusively on financial institutions serving as trusted third parties to process electronic payments. While the system works well enough for most transactions, it still suffers from the inherent weaknesses of the trust based model. Completely non-reversible transactions are not really possible, since financial institutions cannot avoid mediating disputes. The cost of mediation increases transaction costs, limiting the minimum practical transaction size and cutting off the possibility for small casual transactions, and there is a broader cost in the loss of ability to make non-reversible payments for non-reversible services. With the possibility of reversal, the need for trust spreads. Merchants must be wary of their customers, hassling them for more information than they would otherwise need. A certain percentage of fraud is accepted as unavoidable. These costs and payment uncertainties can be avoided in person by using physical currency, but no mechanism exists to make payments over a communications channel without a trusted party.
```

## Step 2
Create a checksum from these three files using the SHA256 hash function:
```
$ shasum -a 256 quote1.txt quote2.txt quote3.txt > checksum.sha
```

## Step 3
The checksum that’s created will contain a unique hash associated with each file specified. Note that the hashes are all the same length despite the varying length quotes:
```
$ cat checksum.sha
b17b22e110b4bc6d4fdb3cdab8c36dfcfb109ef698c891a704f49dfe718523c9  quote1.txt
5d06d7e8b206600cd91674298e61cff6434ba1d3ecbc7bf79c10278f68609965  quote2.txt
4d7429f8a7e553ee12f71dc855c858e2c5d01fa97eb4e40747d90f19166f698f  quote3.txt
```

To verify the data integrity of the files using the checksum simply run the following command:
```
$ shasum -c checksum.sha
quote1.txt: OK
quote2.txt: OK
quote3.txt: OK
```

## Step 4
Now to see the power of using hashes for data integrity, go ahead and modify one of the files ever so slightly. For example, you might change the `quote1.txt` content from:
```
The Times 03/Jan/2009 Chancellor on brink of second bailout for banks
```
To
```
The Times 03/Jan/2008 Chancellor on brink of second bailout for banks
```
This is a very subtle change for the human eye to spot but it will be very obvious after hashing the file and comparing the hashes against the checksum. 
```
$ shasum -c checksum.sha
quote1.txt: FAILED
quote2.txt: OK
quote3.txt: OK
shasum: WARNING: 1 computed checksum did NOT match
```
And if you calculate the hash value of `quote1.txt` you’ll see that the new hash value is completely different: 
```
$ shasum -a 256 quote1.txt
a06b37d9c8929b7c5676f64b5e3d956c724155014eed63accbf961a82bf512ec  quote1.txt
```
Whereas previously its hash value was:
```
b17b22e110b4bc6d4fdb3cdab8c36dfcfb109ef698c891a704f49dfe718523c9  quote1.txt
```
What this means is that you don’t need to know **_what_** has changed to be able to tell that **_something_** has changed. In the same way, web applications can tell that you’ve entered an incorrect password even though they don’t know your password!

## Take Away: Hash Pointer
One idea would be to rename `quote1.txt` to its hash value. This serves two purposes:

1.  Identification
2.  Integrity verification

Thus `quote1.txt` would become:
```
b17b22e110b4bc6d4fdb3cdab8c36dfcfb109ef698c891a704f49dfe718523c9.txt
```
This is useful because not only would we be able to reference the quote by its hash value but we’d also be able to verify the integrity of the quote!

Similarly, in Bitcoin, blocks and transactions are typically referenced using their hash values to take advantage of the two benefits mentioned above.
