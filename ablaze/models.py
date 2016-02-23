import os
from importlib import import_module
from urllib import parse

from aiopg.sa import create_engine
from sqlalchemy import MetaData, Table

# TODO:
# Provide lazy connections
# Close lazy connections
# Provide access to models via app

metadata = MetaData()


async def cleanup(app):
    # Ensure we close the DB pool
    app['db'].close()
    await app['db'].wait_closed()


class ModelsProxy(dict):
    def __init__(self, source):
        super().__init__(source)
        known = {}
        for app, pkg in source.items():
            for name in dir(pkg):
                obj = getattr(pkg, name)
                if not isinstance(obj, Table):
                    continue
                if name in known:
                    known[name] = False
                    continue
                known[name] = obj
        for key, obj in known.items():
            if obj is not False:
                setattr(self, key, obj)


async def setup(app):
    config = app['config']['models']

    app['db'] = await create_engine(**get_db_options())
    app.on_shutdown.append(cleanup)

    models = {}
    modules = [x.strip() for x in config['models'].split(',')]
    for module in modules:
        pkg = import_module(module)
        # Register pkg models into convenience container
        pkg_name = getattr(pkg, 'NAME', module)
        models[pkg_name] = pkg

    app['models'] = ModelsProxy(models)


def get_db_options():
    parse.uses_netloc.append('postgres')
    url = parse.urlparse(os.environ["DATABASE_URL"])
    path = url.path[1:]  # Strip leading /

    return {
        'database': path or None,
        'user': url.username or None,
        'password': url.password or None,
        'host': url.hostname or None,
        'port': url.port or None,
    }
