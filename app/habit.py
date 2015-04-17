from bottle import *
from html_writer import *
import make_cal
import page_outline

STATIC_PATH = './static'

@route('/')
def index():
	return static_file('index.html', root = STATIC_PATH)

@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root = STATIC_PATH)

@route('/favicon.ico')
def favicon():
	return static_file('favicon.ico', root = STATIC_PATH)

@route('/cal')
def cal():
	uuid = request.get_cookie('uuid')
	ukey = request.get_cookie('ukey')
	if uuid == None or ukey == None:
		return static_file('calerror.html', root = STATIC_PATH)
	return str(make_cal.make_cal(uuid, ukey))

@route('/settings')
def settings():
	html = page_outline.get()
	html(
		Tag('form', {'action': '/settings', 'method': 'post'})(
			'UUID: ', Tag('input', {'name': 'uuid', 'type': 'text'}), Tag('br'),
			'API Key: ', Tag('input', {'name': 'ukey', 'type': 'text'}), Tag('br'),
			Tag('input', {'value': 'Save', 'type': 'submit'})
		)
	)
	return str(html)

@route('/settings', method = 'POST')
def settings_post():
	uuid = request.forms.get('uuid')
	ukey = request.forms.get('ukey')
	response.set_cookie('uuid', uuid, max_age = 350000)
	response.set_cookie('ukey', ukey, max_age = 350000)
	html = page_outline.get()
	html(
		Tag('p')('Settings saved'),
		Tag('br'),
		Tag('a', {'href': '/cal'})('Go to Calendar')
	)
	return str(html)

run(host = "0.0.0.0", port = int(os.environ.get("PORT", 80)))