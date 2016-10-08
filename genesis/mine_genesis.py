## Objective: mine the Bitcoin genesis block

from struct import pack
from hashlib import sha256
from codecs import decode
from binascii import hexlify

## The version number 1 as a little-endian (<) unsigned-long (L)
version = pack("<L", 0x01)

## The previous block header hash is 32-bit zero
previous_header_hash = decode("0000000000000000000000000000000000000000000000000000000000000000", 'hex')

## Merkle root (in this case, also a txid). Don't forget to reverse it
## into Internal Byte Order
merkle_root = decode("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b", 'hex')[::-1]

## Date in Unix time format
date = pack("<L", 1231006505)

## nBits is stored as a little-endian (>) unsigned-long (L)
nbits = pack("<L", 0x1d00ffff)

## Bitcoin uses the SHA256d hash function, which is the SHA256 function
## run twice (double).
def sha256d(data):
  return sha256(sha256(data).digest()).digest()

## We want to display our results as hex in RPC Byte Order, so
## we need to reverse the byte order
def internal2rpc(hash):
  return hexlify(hash[::-1])

## Convert current nbits into a big-endian string
nbits_calc = hexlify(nbits[::-1])

## The nbits calculation is base-256
base = 256

## The nbits exponent is the the first byte of the nBits
exponent = int(nbits_calc[0:2], 16) - 3
## The nbits significand is the other three bytes
significand = int(nbits_calc[2:8], 16)

## Do the nbits calculation
target = significand * ( base ** exponent )

## Search for a hash below the target value. We'll limit the nonce range
## here because CPU mining is very slow
nonce = 0x7c2ba836
while nonce < 0x7c2bac1e:
  header = (
	version
	+ previous_header_hash
	+ merkle_root
	+ date
	+ nbits
	+ pack("<L", nonce)
  )

  ## Get the header hash corresponding to the header
  header_hash = sha256d(header)

  ## If the header hash is less than the target, print the results and
  ## break the loop
  if int(hexlify(header_hash[::-1]), 16) < target:
	print("Nonce  	Header Hash")
	print(nonce, internal2rpc(header_hash))
	break

  ## Increment the nonce
  nonce += 1
