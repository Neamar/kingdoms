from kingdom.models import Kingdom, Folk


def kingdom_get_title(self, title):
	try:
		the_folk = Folk.objects.get(title__title__name=title, kingdom=self)
	except Folk.DoesNotExist:
		return None
	return the_folk
Kingdom.get_title = kingdom_get_title
