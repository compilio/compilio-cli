import yaml
import os


class Config:
    def __init__(self):
        self.cfg = None
        self.load_config()

    def load_config(self):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + "/config.yml", 'r') as yml_file:
            self.cfg = yaml.load(yml_file)

    def __getitem__(self, key):
        return self.cfg[key]
