#!/usr/bin/python
import sys
import requests

if __name__ == '__main__':
    cmd = ""
    for i in range(1, len(sys.argv)):
        cmd += sys.argv[i] + " "

    cmd = cmd.strip()
    print(cmd)

    req = requests.post('http://httpbin.org/post', data={'command': cmd})
    print(req)

