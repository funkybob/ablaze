import asyncio
from aiohttp.web import run_app  # NOQA
from .base import build_app  # NOQA


def launch(config_path, defaults=None):
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(
        build_app(loop, config_path, defaults=defaults)
    )
    run_app(app, host='127.0.0.1', port=8080)
