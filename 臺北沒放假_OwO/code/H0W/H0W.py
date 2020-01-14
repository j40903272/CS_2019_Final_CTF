import random
import time
import ctypes


def stay_int(x):
    return ctypes.c_int(x).value

def stay_32bit(x):
    return int('{0:032b}'.format(x)[-32:], 2)

def reverse_ichinokata(x):
    return stay_int(x ^ 0xFACEB00C)

def reverse_ninokata(x):
    return stay_int(x - 74628)

def reverse_sannokata(x):
    a = rightRotate(x & 0xAAAAAAAA, 2)
    b = leftRotate(x & 0x55555555, 4)
    return stay_int(a|b)

def reverse_yonnokata(x):
    x = reverse_sannokata(x)
    x = reverse_ninokata(x)
    return reverse_ichinokata(x)

INT_BITS = 32

def leftRotate(n, d): 
    return stay_32bit((n << d)|(n >> (INT_BITS - d)) )
  
def rightRotate(n, d):
    return stay_32bit((n >> d)|(n << (INT_BITS - d)) & 0xFFFFFFFF)

def reverse_nini5(x, v2):
    v2 = v2%4
    if (v2 == 0):
        result = reverse_ichinokata(x)
    elif (v2 == 1):
        result = reverse_ninokata(x)
    elif (v2 == 2):
        result = reverse_sannokata(x)
    elif (v2 == 3):
        result = reverse_yonnokata(x)
    
    #print(x, v2, result, struct.pack('<i', result))
    return result


from tqdm import tqdm
from terrynini import *

output = open("output.txt", "rb").read()
print(output[-56:][::4])
output = output[:-56]
print(len(output), len(output) // 4)

randNum = open("randomNum.txt", "r").read().split()
randNum = [int(i) for i in randNum]
print(len(randNum))

nini3()
for i, j in tqdm(zip(range(0, len(output), 4), randNum)):
    x = struct.unpack('<i', output[i:i + 4])[0]
    x = reverse_nini5(x, j)
    nini6(x)
