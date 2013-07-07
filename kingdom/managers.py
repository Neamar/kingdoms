from django.db import models


class FolkManager(models.Manager):
	"""
	Default manager for folk, hiding dead people.
	"""
	
	use_for_related_fields = True

	def get_query_set(self):
		return super(FolkManager, self).get_query_set().filter(death=None)
