"""
Calls cron commands
"""
import time
import django.dispatch
from django.core.management.base import BaseCommand
from django.db import transaction

cron_minute = django.dispatch.Signal(providing_args=['counter'])
cron_ten_minutes = django.dispatch.Signal(providing_args=['counter'])


class Command(BaseCommand):
	args = ''
	help = 'Calls crons from each module. This script must be called by a crontab.'

	def handle(self, *args, **options):
		counter = int(time.time() / 60)
		self.minute(counter)

		if counter % 10 == 0:
			self.ten_minutes(counter / 10)

	@transaction.commit_on_success
	def minute(self, counter):
		"""
		Send cron_minute signals.
		Wrap everything in a transaction to ensure ACID.
		"""
		
		cron_minute.send(self, counter=counter)

	@transaction.commit_on_success
	def ten_minutes(self, counter):
		"""
		Send cron__ten_minutes signals.
		Wrap everything in a transaction to ensure ACID.
		"""

		cron_ten_minutes.send(self, counter=counter / 10)
