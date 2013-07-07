# -*- coding: utf-8 -*-
from kingdom.models import Kingdom, Folk
from title.models import Title, AvailableTitle
from django.db import IntegrityError


def kingdom_get_folk_in_title(self, title_slug):
	"""
	Return the folk who got the title, or return none if there is no folk with this title
	"""
	try:
		folk = Folk.objects.get(title__title__slug=title_slug, kingdom=self)
		return folk
	except Folk.DoesNotExist:
		return None
Kingdom.get_folk_in_title = kingdom_get_folk_in_title


def kingdom_unlock_title(self, slug):
	"""
	Unlock the title.
	"""
	title = Title.objects.get(slug=slug)
	try:
		available_title = AvailableTitle(
			title=title,
			kingdom=self
		)
		available_title.save()
	except IntegrityError:
		pass
Kingdom.unlock_title = kingdom_unlock_title


def folk_add_title(self, title_slug):
	"""
	Add the title to the folk
	"""
	available_title = AvailableTitle.objects.get(title__slug=title_slug, kingdom=self.kingdom)
	available_title.folk = self
	available_title.save()
Folk.add_title = folk_add_title


def folk_remove_title(self):
	"""
	Remove the title from the folk
	"""
	try:
		available_title = AvailableTitle.objects.get(kingdom=self.kingdom, folk=self)
	except:
		pass
	available_title.folk = None
	available_title.save()
Folk.remove_title = folk_remove_title
