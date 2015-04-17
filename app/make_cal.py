import datetime
import calendar
import hrpg
import hrpg.api
import markdown
from html_writer import Tag

# This was the original HabitCal thing before I made it a webapp
# It's pretty rough around the edges.

# The task collection should be seperated from the HTML generation :/

def make_cal(uuid, ukey):

	# HabitRPG Stuff

	hapi = hrpg.api.HRPG({'x-api-user': uuid, 'x-api-key': ukey})

	tasks = hapi.user.tasks()

	tasks_by_date = {}

	for i in tasks:
		if i.get('completed') == False and i['type'] == 'todo':
			if 'date' in i:
				datetext = i['date']
				datetext = datetext[:datetext.find('T')]
				dateparts = datetext.split('-')
				dto = datetime.date(int(dateparts[0]), int(dateparts[1]), int(dateparts[2]))
				if dto in tasks_by_date:
					tasks_by_date[dto].append(i['text'])
				else:
					tasks_by_date[dto] = [i['text']]

	# Date stuff

	dto_now = datetime.datetime.now()
	current_date = '{}/{}/{}'.format(dto_now.day, dto_now.month, dto_now.year)

	def getDisplayDates(year, month):
		if month > 12:
			month -= 12
			year += 1
		return calendar.Calendar().itermonthdates(year, month)

	display_dates = set()

	for i in range(1, 13):
		display_dates = display_dates.union(set(getDisplayDates(dto_now.year, i)))

	display_dates = list(display_dates)
	display_dates.sort(key = lambda x: x.day)
	display_dates.sort(key = lambda x: x.month)

	# HTML Stuff

	days_of_week = [
		'Monday',
		'Tuesday',
		'Wednesday',
		'Thursday',
		'Friday',
		'Saturday',
		'Sunday'
	]

	months_of_year_short = [
		'Jan', 'Feb', 'Mar', 'Apr',
		'May', 'Jun', 'Jly', 'Aug',
		'Sep', 'Oct', 'Nov', 'Dec'
	]

	the_table = Tag('table', {'class': 'myTable'})(
		Tag('tr')(
			*[Tag('td')(Tag('p')(i)) for i in days_of_week]
		)
	)

	for i in range(0, len(display_dates), 7):
		row = Tag('tr')
		for j in display_dates[i: i + 7]:
			text = '{} {}'.format(j.day, months_of_year_short[j.month - 1])
			datetext = Tag('p', {'class': 'smallText'})(text)
			markdown_html = ''
			for k in tasks_by_date.get(j, []):
				markdown_html += markdown.markdown(k)
			#tlist = Tag('ul')
			#for k in tasks_by_date.get(j, []):
			#	tlist(Tag('li')(k))
			# text = '{}/{}/{}'.format(j.year, j.month, j.day)
			# print(text)
			cell = Tag('td')(datetext, markdown_html)
			if j.month % 2 == 0:
				cell['class'] = 'lightBackground'
			if j.month == dto_now.month and j.day == dto_now.day:
				cell['class'] = 'blueBackground'
			row(cell)
		the_table(row)

	html_framework = Tag('html')(
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
				Tag('p')(
					'Current Date: ',
					current_date
				),
				the_table
			)
		)
	)

	return str(html_framework)