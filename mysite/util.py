import json
from os.path import join


def get_env(base_dir):
    """ Obtenemos las 'variables de entorno"""
    with open(join(base_dir, '/settings.json')) as f:
        env = json.load(f)
        return env
    return {}
