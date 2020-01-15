from Crypto.Util.number import *

f1 = 93441898286204429250545242618928584261
f2 = 97471567017733473358158950635989199220
f3 = 26749

f = [f1, f2, f3]

for i in range(3):
    k = long_to_bytes(f[i])
    print(k)

