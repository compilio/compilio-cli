#!/usr/bin/python
import os
import sys
import time
import zipfile

import requests

from .config import Config


def get_full_command():
    cmd = ""
    for i in range(1, len(sys.argv)):
        cmd += sys.argv[i] + " "

    cmd = cmd.strip()
    return cmd


def init_task(command, cfg):
    res = requests.post(cfg['compilio_host'] + '/compiler/init',
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

    requests.post(cfg['compilio_host'] + '/compiler/upload',
                  data={'task_id': task_id}, files=files)


def wait_task_termination(task_id):
    while True:
        res = requests.get(cfg['compilio_host'] +
                           '/compiler/task?task_id=' + task_id)
        res_json = res.json()
        if res_json['state'] == 'SUCCESS':
            return res_json

        time.sleep(0.5)


def download_output_files(task_id):
    res = requests.get(cfg['compilio_host'] +
                       '/compiler/get_output_files?task_id=' + task_id)
    if res.status_code == 200:
        filename = 'output.zip'
        with open(filename, 'w+b') as f:
            f.write(res.content)

        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall("./")

        os.remove(filename)


def print_license():
    print("""
Copyright (C) 2017 https://github.com/Compilio
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions; for details see https://compil.io/terms
    """)
    exit(0)


def print_help():
    print("""
Write your command after the compilio keyword (e.g. "compilio pdflatex myfile.tex").
Run "compilio --licence" to see the terms of use.
    """)
    exit(0)


def main():
    cfg = Config()

    command = get_full_command()
    if command == '' or command == '--help':
        print_help()

    if command == '--licence':
        print_license()

    input_files, task_id, res_text = init_task(command, cfg)

    if not input_files:
        print(res_text)
        exit(1)

    upload_files(input_files, task_id)

    res_json = wait_task_termination(task_id)
    print(res_json['output_log'])
    download_output_files(task_id)
    print('You can check your task on the website '
          + cfg['compilio_host'] + '/' + task_id)
