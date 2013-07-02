from kingdom.models import Kingdom, Folk
from title.models import Title, AvailableTitle
from django.db import IntegrityError


def kingdom_get_folk_in_title(self, title):
	"""
	Return the folk who got the title, or return none if there is no folk with this title
	"""
	try:
		the_folk = Folk.objects.get(title__title__name=title, kingdom=self)
	except Folk.DoesNotExist:
		return None
	return the_folk
Kingdom.get_folk_in_title = kingdom_get_folk_in_title


def kingdom_unlock_title(self, title):
	"""
	Unlock the title and return the available_title unlocked
	"""
	try:
		available_title = AvailableTitle(
			title=Title.objects.get(name=title),
			kingdom=self
		)
		available_title.save()
	except IntegrityError:
		available_title = AvailableTitle.objects.get(title__name=title, kingdom=self)
	return available_title
Kingdom.unlock_title = kingdom_unlock_title
