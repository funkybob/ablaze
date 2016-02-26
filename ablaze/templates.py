from aiohttp import web
from knights.loader import TemplateLoader


async def setup(app, config):
    paths = config['paths']
    paths = [x.strip() for x in paths.split(',')]
    app['templates'] = TemplateLoader(paths)


def render(request, template, context={}):
    template = request.app['templates'][template_name]
    return web.Response(text=template(context), content_type='text/html')
