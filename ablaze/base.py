import configparser
from importlib import import_module

from aiohttp import web


async def build_app(loop, config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    app = web.Application(loop=loop)
    app['config'] = config

    modules = [x.strip() for x in config['main']['modules'].split(',')]
    for module in modules:
        if '.' in module:
            pkg = import_module(module)
        else:
            pkg = import_module(module, 'ablaze')
        await pkg.setup(app)
