from bottle import *
from html_writer import *
import make_cal
import page_outline
import sys

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
	timezone = request.get_cookie('timezone')
	# return str(Tag('p')(uuid, '<br>', ukey))
	# timezone = request.get_cookie('timezone')
	if uuid == None or ukey == None:
		with open(STATIC_PATH + '/calerror.html') as f:
			return f.read()
		return '?'
	return str(make_cal.make_cal(uuid, ukey, timezone))

@route('/settings')
def settings():
	html = page_outline.get()
	html(
		Tag('form', {'action': '/settings', 'method': 'post'})(
			'UUID: ', Tag('input', {'name': 'uuid', 'type': 'text'}), Tag('br'),
			'API Key: ', Tag('input', {'name': 'ukey', 'type': 'password'}), Tag('br'),
			'Timezone: ', Tag('input', {'name': 'timezone', 'type': 'number', 'value': 0}), Tag('br'),
			Tag('input', {'value': 'Save', 'type': 'submit'})
		)
		# Tag('br'),
		# Tag('p')(
		# 	'Timezone not thoroughly tested. Be careful with it!'
		# )
	)
	return str(html)

@route('/settings', method = 'POST')
def settings_post():
	COOKIE_TIMEOUT = 700000 # Just over 8 days
	uuid = request.forms.get('uuid')
	ukey = request.forms.get('ukey')
	timezone = request.forms.get('timezone')
	response.set_cookie('uuid', uuid, max_age = COOKIE_TIMEOUT)
	response.set_cookie('ukey', ukey, max_age = COOKIE_TIMEOUT)
	response.set_cookie('timezone', timezone, max_age = COOKIE_TIMEOUT)
	html = page_outline.get()
	html(
		Tag('p')('Settings saved'),
		Tag('br'),
		Tag('a', {'href': '/cal'})('Go to Calendar')
	)
	return str(html)

my_host = "0.0.0.0"
my_port = int(os.environ.get("PORT", 80))

for i in sys.argv[1:]:
	if i.startswith('-host:'):
		my_host = i[6:]
		print('host:', my_host)
	if i.startswith('-port:'):
		my_port = int(i[6:])

print(my_host, my_port)
run(host = my_host, port = my_port)