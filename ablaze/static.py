'''
Add a route handler for static content.

[static]
url = /static/
path = static/

'''

async def setup(app, config):
    app.router.add_static(config['url'], config['path'])
