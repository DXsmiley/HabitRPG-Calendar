import jinja2
import aiohttp
import aiohttp.web
import asyncio
import aiohttp_jinja2
import sys
import os
import markdown

import make_cal
import page_outline


loop = asyncio.get_event_loop()
app = aiohttp.web.Application(loop = loop)


aiohttp_jinja2.setup(app,
	loader = jinja2.FileSystemLoader('./templates/'),
	autoescape = jinja2.select_autoescape(['html', 'xml', 'j2']),
	filters = {
		'markdown': lambda text: jinja2.Markup(markdown.markdown(text))
	}
)


def redirect_to(page):
	async def do_redirect(request):
		return aiohttp.web.HTTPSeeOther('/static/index.html')
	return do_redirect


app.router.add_static('/static', './static')
app.router.add_get('/', redirect_to('/static/index.html'))
app.router.add_get('/favicon.ico', redirect_to('./static/favicon.ico'))


COOKIE_LIFESPAN = 700000 # Just over 8 days


@aiohttp_jinja2.template('calendar.html')
async def page_cal(request):
	uuid = request.cookies.get('uuid')
	ukey = request.cookies.get('ukey')
	timezone = request.cookies.get('timezone')
	remember = request.cookies.get('remember')
	return {'weeks': make_cal.make_cal(uuid, ukey, timezone)}
app.router.add_get('/calendar', page_cal)
app.router.add_get('/cal', redirect_to('/calendar'))


async def settings_post(request):
	form = await request.post()
	remember = form.get('remember')
	uuid = form.get('uuid')
	ukey = form.get('ukey')
	print('Remember: ', remember)
	timezone = form.get('timezone')
	if remember:
		cookie_timeout = COOKIE_LIFESPAN
	else:
		cookie_timeout = None # End of browser session
	response = aiohttp.web.HTTPSeeOther('/calendar')
	response.set_cookie('uuid', uuid, max_age = cookie_timeout)
	response.set_cookie('ukey', ukey, max_age = cookie_timeout)
	response.set_cookie('timezone', timezone, max_age = cookie_timeout)
	response.set_cookie('remember', 'yes', max_age = cookie_timeout)
	return response
app.router.add_post('/settings', settings_post)


if __name__ == '__main__':
	p = os.getenv('PORT')
	aiohttp.web.run_app(app, host = '0.0.0.0', port = int(p) if p else 5000)
