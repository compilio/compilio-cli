#!/usr/bin/python
import sys

import requests

from config import Config


def get_full_command():
    cmd = ""
    for i in range(1, len(sys.argv)):
        cmd += sys.argv[i] + " "

    cmd = cmd.strip()
    return cmd


if __name__ == '__main__':
    cfg = Config()

    command = get_full_command()
    print(command)

    res = requests.post(cfg['compilio_host'] + 'compiler/init',
                        data={'command': command})
    if res.status_code == 200:
        json = res.json()
        input_files = json['input_files']
        task_id = json['task_id']

        files = {}
        file_index = 0
        for input_file_path in input_files:
            files[str(file_index)] = open(input_file_path, 'rb')
            file_index += 1

        res = requests.post(cfg['compilio_host'] + 'compiler/upload',
                            data={'task_id': task_id}, files=files)
        print(res)
    else:
        print(res.text)

        # TODO : More readable -> Create functions
        # TODO : Query compilio/status at fixed time
        # TODO : Get output_files when 'terminated'
