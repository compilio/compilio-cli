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

    res = requests.post(cfg['compilio_host'] + 'compiler/init', data={'command': cmd})
    if res.status_code == 200:
        json = res.json()
        input_files = json['input_files']
        task_id = json['task_id']

        files = {}
        i = 0
        for input_file_path in input_files:
            files[str(i)] = open(input_file_path, 'rb')

        res = requests.post(cfg['compilio_host'] + 'compiler/upload', data={'task_id': task_id}, files=files)
        print(res)
    else:
        print(res.text)

