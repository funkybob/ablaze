from aiohttp import web
from knights.loader import TemplateLoader


async def setup(app):
    config = app['config']['templates']
    paths = config['paths']
    paths = [x.strip() for x in paths.split(',')]
    app['templates'] = TemplateLoader(paths)


def render(request, template, context={}):
    tmpl = request.app['templates'][template]
    return web.Response(text=tmpl(context), content_type='text/html')
