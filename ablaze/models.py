import os
from importlib import import_module
from urllib import parse

from aiopg.sa import create_engine

# TODO:
# Provide lazy connections
# Close lazy connections
# Provide access to models via app

async def cleanup(app):
    # Ensure we close the DB pool
    app['db'].close()
    await app['db'].wait_closed()


async def setup(app):
    config = app['config']['models']

    app['db'] = await create_engine(**get_db_options())
    app.on_shutdown.append(cleanup)

    modules = [x.strip() for x in config['models']]
    for module in modules:
        pkg = import_module(module)
        # Register pkg models into convenience container


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
