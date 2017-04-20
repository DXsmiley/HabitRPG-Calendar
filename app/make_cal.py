import datetime
import calendar
import markdown
import page_outline
import traceback
import re
import requests
import json
from html_writer import Tag

def get_tasks(uuid, ukey, time_offset):
	heads = {
		'x-api-user': uuid,
		'x-api-key': ukey,
		'content-type': 'application/json'
	}
	r = requests.get('https://habitica.com/api/v3/tasks/user', headers = heads)
	tasks = json.loads(str(r.content, encoding = 'utf-8'))
	tasks = tasks['data']
	tasks_by_date = {}
	for i in tasks:
		if i.get('completed') == False and i['type'] == 'todo':
			if 'date' in i:
				datetext = i['date']
				if datetext != None:
					dateparts = re.split(r'\-|\:|\.|T|Z', datetext)
					dateparts = [int(i) for i in dateparts if i.isnumeric()]
					dto = datetime.datetime(dateparts[0], dateparts[1], dateparts[2], dateparts[3])
					# This should fix the off-by-one issue.
					dto += datetime.timedelta(hours = 12)
					item = (i['text'], i['notes'])
					dto = dto.date() # Remove the time part.
					if dto in tasks_by_date:
						tasks_by_date[dto].append(item)
					else:
						tasks_by_date[dto] = [item]
	return tasks_by_date

def get_display_dates():

	this_year = datetime.datetime.now().year

	def dates_for_month(year, month):
		if month > 12:
			month -= 12
			year += 1
		return calendar.Calendar().itermonthdates(year, month)

	display_dates = set()

	for i in range(1, 13):
		display_dates = display_dates.union(set(dates_for_month(this_year, i)))

	display_dates = list(display_dates)
	display_dates.sort(key = lambda x: x.day)
	display_dates.sort(key = lambda x: x.month)
	display_dates.sort(key = lambda x: x.year)

	return display_dates


MONTHS_OF_YEAR_SHORT = [
	'Jan', 'Feb', 'Mar', 'Apr',
	'May', 'Jun', 'Jly', 'Aug',
	'Sep', 'Oct', 'Nov', 'Dec'
]


# TODO: Rename to something more accurate
def make_cal(uuid, ukey, timezone):

	timezone_delta = datetime.timedelta(hours = int(timezone))

	dto_now = datetime.datetime.now()
	dto_now += timezone_delta
	current_date = '{}/{}/{}'.format(dto_now.day, dto_now.month, dto_now.year)

	display_dates = get_display_dates()

	tasks_by_date = get_tasks(uuid, ukey, timezone_delta)

	weeks = [
		[
			{
				'name': '{} {}'.format(day.day, MONTHS_OF_YEAR_SHORT[day.month - 1]),
				'tasks': tasks_by_date.get(day, []),
				'month': day.month
			}
			for day in week
		]
		for week in (display_dates[i:i+7] for i in range(0, len(display_dates), 7))
	]

	return weeks
