
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage


async def setup(app, config):
    session_setup(app, EncryptedCookieStorage(config['secret'].encode('utf-8')))
