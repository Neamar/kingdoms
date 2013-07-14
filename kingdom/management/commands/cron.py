"""
Calls cron commands
"""
import time
import django.dispatch
from django.core.management.base import BaseCommand

cron_minute = django.dispatch.Signal(providing_args=['counter'])
cron_ten_minutes = django.dispatch.Signal(providing_args=['counter'])


class Command(BaseCommand):
	args = ''
	help = 'Calls crons from each module. This script must be called by a crontab.'

	def handle(self, *args, **options):
		counter = int(time.time() / 60)
		cron_minute.send(self, counter=counter)

		if counter % 10 == 0:
			cron_ten_minutes.send(self, counter=counter / 10)
