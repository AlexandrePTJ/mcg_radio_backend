from aiohttp import web
import aiohttp_jinja2
import jinja2


class RadiosView(web.View):

    MAX_RADIOS = 6

    @aiohttp_jinja2.template('radios.html')
    async def get(self):
        radios = self.request.app['PlaybackController'].radios
        if len(radios) < self.MAX_RADIOS:
            for idx in range(len(radios) + 1, self.MAX_RADIOS):
                radios.append({ 'label': '', 'url': '', 'index': idx })
        return { 'radios': radios }

    async def post(self):
        data = await self.request.post()
        print(data)
        return web.HTTPFound('/')


def make_webapp(playback_controller):
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app.router.add_static('/static', 'static')
    app.router.add_route('*', '/', RadiosView)
    app['PlaybackController'] = playback_controller
    return app
