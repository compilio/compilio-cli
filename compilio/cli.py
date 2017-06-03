#!/usr/bin/python
import argparse
import os
import sys
import time
import zipfile

import requests
from requests.exceptions import ConnectionError

from .config import Config


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
    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    def next_spin(spinner):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')

    spinner = spinning_cursor()
    spinner_speed = 0.1
    status_update_delay = 1.0
    waited_time = 999.0

    printed_log = ''

    while True:
        time.sleep(spinner_speed)
        next_spin(spinner)
        waited_time += spinner_speed

        if waited_time >= status_update_delay:
            waited_time = 0
            try:
                res = requests.get(cfg['compilio_host'] +
                                   '/compiler/task?task_id=' + task_id)
            except ConnectionError:
                print('Connection error : cannot reach ' + cfg['compilio_host'] + ' on status check')
                exit(1)

            res_json = res.json()

            logs = res_json['output_log']
            print(logs.replace(printed_log, ''), end="")
            printed_log = logs

            if res_json['state'] == 'FAILED':
                print('Compilation failed.')
                exit(1)

            if res_json['state'] == 'SUCCESS':
                return res_json


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


def main():
    class ComputeCommand(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            try:
                setattr(namespace, self.dest, ' '.join(values))
            except TypeError:
                pass

            args = vars(namespace)

            if args['license']:
                print_license()

            cfg = Config()
            command = args['command']
            if command is None or command == '':
                parser.print_help()

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

    parser = argparse.ArgumentParser(
        description='Compilio, Write your command after the compilio keyword (e.g. "compilio pdflatex myfile.tex")')
    parser.add_argument('command', help='Input command', nargs='*', action=ComputeCommand)
    parser.add_argument('--license', '-l', help='Show license and terms of use', action='store_true')
    parser.add_argument('--verbose', '-v', help='Show debug logs', action='store_true')

    parser.parse_args()
