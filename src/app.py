import logging
import os
from datetime import datetime

from aiohttp import web, ClientSession

name = os.getenv('NAME', '<name-unknown>')
other = os.getenv('OTHER', None)
if other:
    other_url = 'http://{}/info'.format(other)
else:
    other_url = None

logger = logging.getLogger('std')
logger.setLevel(logging.INFO)
hdl = logging.StreamHandler()
hdl.setLevel(logging.INFO)
hdl.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(hdl)


async def index(request):
    logger.info('index: %s', request)
    status, text = None, None
    if other_url:
        logger.info('connecting to %s', other_url)
        async with ClientSession() as session:
            async with session.get(other_url, timeout=5) as r:
                status = r.status
                text = await r.text()
    return web.Response(text="""\
this:
  name: {name}
other:
  url: {url}
  status: {status}
  text: {text}""".format(name=name, url=other_url, status=status, text=text))


async def info(request):
    logger.info('info: %s', request)
    return web.Response(text='this is {name} {dt}'.format(name=name, dt=datetime.now()))


app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/info', info)

if __name__ == '__main__':
    web.run_app(app, port=80, shutdown_timeout=1, print=logger.info)
