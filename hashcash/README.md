# Hashcash

**Play-by-play:** [Hashcash Demo](http://showterm.io/6da51cbe00931ceb6dc77)

## Minting a stamp
To “mint” a stamp you can run the following command:
```
$ hashcash -m -r justin@nospam.com
hashcash stamp: 1:20:160930:justin@nospam.com::hCiehBcv/W90Bpce:000000000000000000000000000000000000000000004YEQ
```
The important part here is the random string `hCiehBcv/W90Bpce`

There was clearly "proof of work" in generating the stamp since there is partial collision that could have only been produced via brute force. We can verify the partial collision by hashing the stamp using SHA-1 to observe the leading zeroes:
```
$ echo -n "1:20:160930:justin@nospam.com::hCiehBcv/W90Bpce:000000000000000000000000000000000000000000004YEQ" | shasum -t
000000efe42fb212d4268aa44af912a26ce1c47e
```

Now let's create a stamp using the default 20 bits, which equates to five leading zeroes, and save it as a file
```
$ hashcash -m -r justin@nospam.com > stamp
$ echo -n $( cat stamp ) | shasum
00000a0b04416b6367f3d1954b7569540d0ab04c
```

To get 7 zeroes, we’ll need 28 bits (7 * 4)
```
$ hashcash -b 28 -m -r justin@nospam.com > foreverstamp
$ echo -n $( cat foreverstamp ) | shasum
0000000d8e4c26fb1e63c992885db80bf11e9803
```
