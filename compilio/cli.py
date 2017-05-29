#!/usr/bin/python
import argparse
import os
import sys
import time
import zipfile

import requests
from requests.exceptions import ConnectionError

from .config import Config


def get_full_command():
    cmd = ""
    for i in range(1, len(sys.argv)):
        cmd += sys.argv[i] + " "

    cmd = cmd.strip()
    return cmd


def init_task(command, cfg):
    try:
        res = requests.post(cfg['compilio_host'] + '/compiler/init',
                            data={'command': command})
    except ConnectionError:
        print('Connection error : cannot reach ' + cfg['compilio_host'] + ' on init')
        exit(1)

    if res.status_code != 200:
        return [False, False, res.text]

    json = res.json()
    input_files = json['input_files']
    task_id = json['task_id']
    return [input_files, task_id, res.text]


def upload_files(input_files, task_id, cfg):
    files = {}
    file_index = 0
    for input_file_path in input_files:
        files[str(file_index)] = open(input_file_path, 'rb')
        file_index += 1

    try:
        requests.post(cfg['compilio_host'] + '/compiler/upload',
                      data={'task_id': task_id}, files=files)
    except ConnectionError:
        print('Connection error : cannot reach ' + cfg['compilio_host'] + ' on upload')
        exit(1)


def wait_task_termination(task_id, cfg):
    while True:
        try:
            res = requests.get(cfg['compilio_host'] +
                               '/compiler/task?task_id=' + task_id)
        except ConnectionError:
            print('Connection error : cannot reach ' + cfg['compilio_host'] + ' on status check')
            exit(1)

        res_json = res.json()

        if res_json['state'] == 'FAILED':
            print('Compilation failed.')
            exit(1)

        if res_json['state'] == 'SUCCESS':
            return res_json

        time.sleep(0.5)


def download_output_files(task_id, cfg):
    try:
        res = requests.get(cfg['compilio_host'] +
                           '/compiler/get_output_files?task_id=' + task_id)
    except ConnectionError:
        print('Connection error : cannot reach ' + cfg['compilio_host'] + ' on download')
        exit(1)

    if res.status_code == 200:
        filename = 'output.zip'
        with open(filename, 'w+b') as f:
            f.write(res.content)

        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall("./")

        os.remove(filename)


def print_output_log(output_log):
    print('\nOutput logs:')
    print(' 🌧   '.join(('\n' + output_log.lstrip()).splitlines(True)))


def print_task_link(task_id, cfg):
    print('You can check your task on the website '
          + cfg['compilio_host'] + '/task/' + task_id)


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
    class MyAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, ' '.join(values))

            cfg = Config()
            command = vars(namespace)['command']
            if command == '' or command == '--help':
                print_help()

            if command == '--licence':
                print_license()

            input_files, task_id, res_text = init_task(command, cfg)

            if not input_files:
                print(res_text)
                exit(1)

            upload_files(input_files, task_id, cfg)

            print_task_link(task_id, cfg)

            res_json = wait_task_termination(task_id, cfg)
            print_output_log(res_json['output_log'])
            download_output_files(task_id, cfg)

            print_task_link(task_id, cfg)

    parser = argparse.ArgumentParser(description='Compilio')
    parser.add_argument('command', help='Input command', nargs='+', action=MyAction)
    parser.add_argument('--licence', '-l', help='Show license', action='store_true')

    parser.parse_args()
