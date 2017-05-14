#!/usr/bin/python
import sys

import requests

from config import Config

if __name__ == '__main__':
    cfg = Config()

    cmd = ""
    for i in range(1, len(sys.argv)):
        cmd += sys.argv[i] + " "

    cmd = cmd.strip()
    print(cmd)

    res = requests.post(cfg['compilio_host'] + 'compiler/init',
                        data={'command': cmd})
    if res.status_code == 200:
        json = res.json()
        input_files = json['input_files']
        task_id = json['task_id']

        files = {}
        i = 0
        for input_file_path in input_files:
            files[str(i)] = open(input_file_path, 'rb')

        res = requests.post(cfg['compilio_host'] + 'compiler/upload',
                            data={'task_id': task_id}, files=files)
        print(res)
    else:
        print(res.text)

        # TODO : More readable -> Create functions
        # TODO : Query compilio/status at fixed time
        # TODO : Get output_files when 'terminated'
