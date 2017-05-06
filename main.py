#!/usr/bin/python
import sys
import requests
import yaml

if __name__ == '__main__':

    with open("config.yml", 'r') as yml_file:
        cfg = yaml.load(yml_file)

    cmd = ""
    for i in range(1, len(sys.argv)):
        cmd += sys.argv[i] + " "

    cmd = cmd.strip()
    print(cmd)

    req = requests.post(cfg['compilio_host'] + 'compiler/init', data={'command': cmd})
    print(req)

