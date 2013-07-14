"""
Calls cron commands
"""
import datetime
import django.dispatch

cron_minute = django.dispatch.Signal(providing_args=[])
cron_ten_minutes = django.dispatch.Signal(providing_args=[])


class Command(BaseCommand):
	args = ''
	help = 'Calls crons from each module. This script must be called by a crontab.'

	def handle(self, *args, **options):
		cron_minute.send()
