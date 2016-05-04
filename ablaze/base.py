import configparser
import os
from importlib import import_module

from aiohttp import web

from .config import EnvironInterpolation

import logging
log = logging.getLogger(__name__)


async def build_app(loop, config_path, defaults=None):
    config_path = os.path.abspath(config_path)
    if defaults is None:
        defaults = {}
    # defaults.setdefault('CONFIG_DIR', os.path.dirname(config_path))
    config = configparser.ConfigParser(interpolation=EnvironInterpolation(), defaults=defaults)
    config.read(config_path)

    app = web.Application(loop=loop)
    app['config'] = config

    modules = config['ablaze']
    for key, module in modules.items():
        log.info('Loading modul: %s -> %s', module, key)
        cfg = config[key]
        pkg = import_module(module, 'ablaze')
        await pkg.setup(app, cfg)

    return app
