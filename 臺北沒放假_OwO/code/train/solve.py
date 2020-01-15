from pwn import *
from Crypto.Util.number import *

port = 20002
host = 'eductf.zoolab.org'
r = remote( host, port)

r.recvuntil('> ')
r.sendline('1')

N = str(r.recvline(), 'utf-8').strip().split()[2]
N = int(N)

r.recvline()
e = 3

cstr = bytes.fromhex(str(r.recvline(), 'utf-8').strip().split()[2])
c = [ bytes_to_long(cstr[i:i+128]) for i in range(0, len(cstr), 128)]

msg = 'date:2019/1/11|session:' + "A"*10 + "|secret:FLAG{"
print(N)
for i in c:
    print(i)

