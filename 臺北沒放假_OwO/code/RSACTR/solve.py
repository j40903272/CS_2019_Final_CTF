from pwn import *
from Crypto.Util.number import *
import numpy as np

port = 20000
host = 'eductf.zoolab.org'

r = remote( host, port)
e = 3

r.recvuntil('> ')
r.sendline('1')
N = int(str(r.recvline(), 'utf-8').strip().split()[2], 10)

r.recvuntil('> ')
r.sendline('3')
r.recvuntil('= ')

bnum = 3
msg = "00" * 16 * bnum

r.sendline(msg)
nonce = str(r.recvline(), 'utf-8').strip().split()[2]
bk = 256
arr = []
carr = []
bias1 = []

for i in range(bnum):
    tmp = bytes.fromhex( nonce[i*bk: i*bk+bk])
    tmp = int.from_bytes(tmp, "big")
    arr.append(tmp)


nonce = pow( arr[-1], 3, N)
r.recvuntil('> ')
r.sendline('2')
c = str(r.recvline(), 'utf-8').strip().split()[2]
cbn = len(c)//bk
r.close()

for i in range(cbn):
    tmp = bytes.fromhex( c[i*bk: i*bk+bk])
    tmp = int.from_bytes(tmp, "big")
    carr.append(tmp)

print(N)
print(nonce)
for i in range(cbn):
    print(carr[i])
