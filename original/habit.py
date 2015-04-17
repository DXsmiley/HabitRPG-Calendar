from bottle import *
from html_writer import *
import make_cal

@route('/')
def index():
	return static_file('index.html', root='./static')

@route('/settings')
def settings():
	html = Tag('html')(
		Tag('head')(
			Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/normalise.css'}),
			Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/style.css'}),
			Tag('title')(
				'HabitRPG Calendar'
			)
		),
		Tag('body')(
			Tag('div', {'class': 'container'})(
				Tag('h1')(
					'HabitRPG Calendar'
				),
				Tag('form', {'action': '/settings', 'method': 'post'})(
					'UUID: ', Tag('input', {'name': 'uuid', 'type': 'text'}), Tag('br'),
					'API Key: ', Tag('input', {'name': 'ukey', 'type': 'text'}), Tag('br'),
					Tag('input', {'value': 'Save', 'type': 'submit'})
				)
			)
		)
	)
	return str(html)

@route('/settings', method = 'POST')
def settings_post():
	uuid = request.forms.get('uuid')
	ukey = request.forms.get('ukey')
	response.set_cookie('uuid', uuid)
	response.set_cookie('ukey', ukey)
	html = Tag('html')(
		Tag('head')(
			Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/normalise.css'}),
			Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/style.css'}),
			Tag('title')(
				'HabitRPG Calendar'
			)
		),
		Tag('body')(
			Tag('div', {'class': 'container'})(
				Tag('h1')(
					'HabitRPG Calendar'
				),
				Tag('p')('Settings saved'),
				Tag('br'),
				Tag('a', {'href': '/cal'})('Go to Calendar')
			)
		)
	)
	return str(html)

@route('/cal')
def cal():
	uuid = request.get_cookie('uuid')
	ukey = request.get_cookie('ukey')
	return str(make_cal.make_cal(uuid, ukey))

@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='./static')

@route('/favicon.ico')
def favicon():
	return static_file('favicon.ico', root='./static')

run(host = 'http://peaceful-hollows-4154.herokuapp.com', port = 80)
