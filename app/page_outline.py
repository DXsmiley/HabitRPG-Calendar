from html_writer import Tag

def get():
	target = Tag('div', {'class': 'container'})(
		Tag('h1')(
			'HabitRPG Calendar'
		)
	)
	framework = Tag('html')(
		Tag('head')(
			Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/normalise.css'}),
			Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/style.css'}),
			Tag('title')(
				'HabitRPG Calendar'
			)
		),
		Tag('body')(
			target
		)
	)
	framework.set_insert_point(target)
	return framework