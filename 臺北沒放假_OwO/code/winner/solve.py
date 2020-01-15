from pwn import *
import numpy as np
import random


port = 20003
host = 'eductf.zoolab.org'

r = remote( host, port)

money = 1.1
poly = 0xaa0d3a677e1be0bf
ptr = 0
idx = []
status = [ 1<<i for i in range(64)]
history = []

def gs( vec, res):
    ans = [ res[i] for i in range(64)]

    for i in range(64):
        if vec[i][i] != 1:
            for j in range(i+1, 64):
                if vec[j][i] == 1:
                    vec[i], vec[j] = vec[j], vec[i]
                    ans[i], ans[j] = ans[j], ans[i]
                    break

        for j in range( 64):
            if vec[j][i] == 1 and i != j:
                for k in range(64):
                    vec[j][k] ^= vec[i][k]

                ans[j] ^= ans[i]

    f = 0
    for i in range(64):
        for j in range(64):
            if i == j and vec[i][j] != 1:
                f = 1
            if i != j and vec[i][j] != 0:
                f = 1
    if (f):
        print("QQ")

    return ans

def step():
    global status, idx, poly, ptr, history
    for _ in range(43):
        ptr = (ptr + 1) % 64
        for i in idx:
            if i != 63:
                status[(ptr+i) % 64] ^= status[(ptr-1) % 64]
    history.append(status[(ptr-1)%64])


def compute():
    global true, status, ptr
    step()
    val = status[(ptr-1) % 64]
    ans = 0
    for i in range(64):
        if (1<<i) & val != 0:
            ans ^= true[i]
    return ans

for i in range(64):
    if (1 << i) & poly != 0:
        idx.append(i)

hnum = 64
for i in range(hnum):
    step()

hvec = []

for i in range(hnum):
    tmp = [ (history[i] & (1<<j)) >> j for j in range(64) ]
    hvec.append(tmp)

rec = []
num = 0
flag = 1
true = []

while(flag):
    msg = r.recvuntil(' ')
    if msg[0] == 62:
        if num < 64:
            guess = random.randint(0, 1) % 2
        else:
            guess = compute()

        r.sendline(str(guess))
        tmoney = float(str( r.recvline(), 'utf-8').strip())
        ans = 0
        if tmoney > money:
            ans = guess
        else:
            ans = 1^guess

        money = tmoney
        rec.append(ans)
        num = num+1

        if num == 64:
            true = gs(hvec, rec)
        if num > 64:
            print(guess, ans, num - 1)

    else:
        msg2 = r.recvline()
        print(msg)
        print(msg2)
        if len(msg2) > 10:
            print(r.recvline())
        flag = 0
        print(num)
