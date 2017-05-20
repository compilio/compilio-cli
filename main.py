#!/usr/bin/python
import sys
import time

import requests

from config import Config


def get_full_command():
    cmd = ""
    for i in range(1, len(sys.argv)):
        cmd += sys.argv[i] + " "

    cmd = cmd.strip()
    return cmd


def init_task(command):
    res = requests.post(cfg['compilio_host'] + 'compiler/init',
                        data={'command': command})

    if res.status_code != 200:
        return [False, False, res.text]

    json = res.json()
    input_files = json['input_files']
    task_id = json['task_id']
    return [input_files, task_id, res.text]


def upload_files(input_files, task_id):
    files = {}
    file_index = 0
    for input_file_path in input_files:
        files[str(file_index)] = open(input_file_path, 'rb')
        file_index += 1

    requests.post(cfg['compilio_host'] + 'compiler/upload',
                  data={'task_id': task_id}, files=files)


def wait_task_termination(task_id):
    while True:
        res = requests.get(cfg['compilio_host'] +
                           'compiler/task?id=' + task_id)
        res_json = res.json()
        if res_json['state'] == 'SUCCESS':
            return res_json

        time.sleep(0.5)


if __name__ == '__main__':
    cfg = Config()

    command = get_full_command()
    print(command)

    input_files, task_id, res_text = init_task(command)

    if not input_files:
        print(res_text)
        exit(1)

    upload_files(input_files, task_id)

    res_json = wait_task_termination(task_id)
    print(res_json['output_log'])
