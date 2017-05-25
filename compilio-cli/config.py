import yaml


class Config:
    def __init__(self):
        self.cfg = None
        self.load_config()

    def load_config(self):
        with open("config.yml", 'r') as yml_file:
            self.cfg = yaml.load(yml_file)

    def __getitem__(self, key):
        return self.cfg[key]
