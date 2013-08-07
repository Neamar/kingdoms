"""
Freeze specified kingdom.
"""
from django.core.management.base import BaseCommand
from django.core import serializers

from kingdom.models import Kingdom


class Command(BaseCommand):
	args = '<kingdom_id kingdom_id>'
	help = 'Create a new freeze for the kingdom.'

	datas = ['']

	def handle(self, *args, **options):
		if len(args) != 1:
			self.stderr.write("Specifiy the id of the kingdom to freeze.")
			return

		# Retrieve the kingdom
		kingdom = Kingdom.objects.get(pk=args[0])

		objects = [kingdom]
		objects += kingdom._kingdomvariable_set.all()
		objects += kingdom.folk_set.all()
		objects += kingdom.availablemission_set.all()
		objects += kingdom.availabletitle_set.all()

		for pending_event in kingdom.pendingevent_set.all():
			objects.append(pending_event)
			objects += pending_event._pendingeventvariable_set.all()

		for pending_mission in kingdom.pendingmission_set.all():
			objects.append(pending_mission)
			objects += pending_mission._pendingmissionvariable_set.all()

		serializers.serialize('json', objects, indent=2, stream=self.stdout)
