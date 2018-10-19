import os
from collections import OrderedDict
from ruamel import yaml

data = {}
for item in ('.mavenlink.yml',
             os.path.expanduser('~/.mavenlink.yml')):

    if os.path.exists(item):
        with open(item, 'r') as f:
            yaml_data = yaml.load(f, Loader=yaml.Loader)
            data.update(yaml_data)

data = OrderedDict(data)

class DotConfig:
    def __init__(self, cfg):
        self.v = None
        self._cfg = cfg

    def __getattr__(self, k):
        self.v = self._cfg[k]
        if isinstance(self.v, dict):
            return DotConfig(self.v)
        return self.v
    def __str__(self):
        return self.v

conf = DotConfig(data)