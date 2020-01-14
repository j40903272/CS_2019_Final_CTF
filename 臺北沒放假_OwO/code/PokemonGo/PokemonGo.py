import string
charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
ans = [185, 212, 172, 145, 185, 212, 172, 177, 217, 212, 204, 177, 185, 212, 204, 209, 161, 124, 172, 177]

for char in charset:
    guess = [ord(char)]
    for i in range(20):
        tmp = ans[i]-guess[-1]
        if chr(tmp) not in charset:
            break
        guess.append(tmp)
        
    if i < 19:
        continue
    guess = guess[:-1]
    print("FLAG{" + "".join([chr(i) for i in guess]) + "}")