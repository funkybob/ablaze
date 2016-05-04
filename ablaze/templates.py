from aiohttp import web
from knights.loader import TemplateLoader


async def setup(app, config):
    paths = config['paths']
    paths = [x.strip() for x in paths.split(',')]
    app['templates'] = TemplateLoader(paths)


def render(request, template_name, context={}):
    template = request.app['templates'][template_name]
    return web.Response(text=template(context), content_type='text/html')


async def stream(request, template_name, context={}):
    resp = web.StreamResponse()
    resp.headers[web.hdrs.CONTENT_TYPE] = 'text/html'
    await resp.prepare(request)

    template = request.app['templates'][template_name]
    for chunk in template._iterator(context):
        resp.write(chunk)
        await resp.drain()

    return resp
