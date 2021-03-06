from string import ascii_letters, digits
from random import choices
from os.path import join
from os import environ
import json
from sys import stderr


SLUG_CHAR = ascii_letters + digits

# Parse config
CONFIG_PATHS = [join(environ.get('XDG_CONFIG_HOME',
                                 environ.get('HOME', './')),
                     'taigalink.json'),
                '/etc/taigalink.json',
                './taigalink.json']

DEFAULT_CONFIG = {'slug_size': 6,
                  'max_paste_size': 1024 * 8,
                  'paste_dir': 'uploads/',
                  'short_dir': 'shorts/',
                  'shortie_route_prefix': '/s/',  # must start and end with /
                  'pasty_route_prefix': '/p/',  # must start and end with /
                  'scheme': 'http',
                  'listen_addr': '127.0.0.1',
                  'port': 1997}


config = DEFAULT_CONFIG.copy()
config_loaded = False
for config_path in CONFIG_PATHS:
    try:
        with open(config_path, 'r') as c:
            config = {**DEFAULT_CONFIG, **json.load(c)}
            config_loaded = True
            break
    except FileNotFoundError:
        pass

if not config_loaded:
    print('WARNING: No config loaded; using defaults.',
          file=stderr)
    try:
        with open('./taigalink.json', 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
            print('WARNING: wrote default config to working directory.',
                  file=stderr)
    except Exception:
        pass

if not config['shortie_route_prefix'].endswith('/') or \
   not config['shortie_route_prefix'].startswith('/'):
    raise RuntimeError('shortie Route Prefix must start and end with a /')
if not config['pasty_route_prefix'].endswith('/') or \
   not config['pasty_route_prefix'].startswith('/'):
    raise RuntimeError('pasty Route Prefix must start and end with a /')


def create_slug(length=config['slug_size']):
    return ''.join(choices(SLUG_CHAR, k=length))
