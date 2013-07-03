# -*- coding: utf-8 -*-
from kingdom.models import Kingdom, Folk
from title.models import Title, AvailableTitle
from django.db import IntegrityError


def kingdom_get_folk_in_title(self, title):
	"""
	Return the folk who got the title, or return none if there is no folk with this title
	"""
	try:
		the_folk = Folk.objects.get(title__title__name=title, kingdom=self)
		return the_folk
	except Folk.DoesNotExist:
		return None
Kingdom.get_folk_in_title = kingdom_get_folk_in_title


def kingdom_unlock_title(self, title):
	"""
	Unlock the title and return the available_title unlocked
	"""
	title = Title.objects.get(name=title)
	try:
		available_title = AvailableTitle(
			title=title,
			kingdom=self
		)
		available_title.save()
	except IntegrityError:
		pass
Kingdom.unlock_title = kingdom_unlock_title


def folk_add_title(self, title_name):
	"""
	Add the title to the folk
	"""
	available_title = AvailableTitle.objects.get(title__name=title_name, kingdom=self.kingdom)
	available_title.folk = self
	available_title.save()
Folk.add_title = folk_add_title
