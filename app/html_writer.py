# Python HTML writing library

import copy

class Tag():

	def __init__(self, name, params = {}):
		self.name = str(name)
		self.params = copy.copy(params)
		self.contents = []
		self.insert_point = None

	def __call__(self, *args):
		if self.insert_point == None:
			self.contents += args
		else:
			self.insert_point(*args)
		return self

	def __setitem__(self, key, value):
		self.params[key] = value

	def __getitem__(self, key):
		return self.params[key]

	def __str__(self):
		# Parameters
		p = ' ' + ' '.join('{}="{}"'.format(k, v) for k, v in self.params.items())	
		if len(self.contents) == 0:
			s = '<{} {} \>\n'.format(self.name, p)
		else:
			# Opening tag
			s = '<' + self.name + '{}>\n'
			# Insert parameters
			s = s.format('' if p == ' ' else p)
			# Indented contents for readable HTML
			c = ''
			for i in self.contents:
				c += str(i)
			l = c.split('\n')
			s += '\n'.join('    ' + i for i in l)
			# Ending tag
			s += '\n</' + self.name + '>\n'
		return s

	def set_insert_point(self, place):
		self.insert_point = place
		return self

if __name__ == '__main__':

	# Construct a 4 by 4 table
	the_table = Tag('table', {'style': 'width:100%', 'border': 1}) (
		*[ Tag('tr')(
				*[ Tag('td')(
						'{} {}'.format(i, j)
					)
				for j in range(4) ]
			)
		for i in range(4) ] 
	)

	# Construct the rest of the page, and put the table in it
	html = Tag('html')(
		Tag('head')(
			Tag('link', {'rel':'stylesheet', 'type':'text/css', 'href':'mystyle.css'}),
			Tag('title')(
				'Example Page',
			)
		),
		Tag('body', {'background': '#FF0000'})(
			Tag('h1')(
				'This is a headding'
			),
			Tag('p')(
				'This is a paragraph'
			),
			the_table
		)
	)

	# Display the HTML code and write it to a file
	code = str(html)
	print(code)
	with open('html_example.html', 'w') as f:
		f.write(code)