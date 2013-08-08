from title.serializers import serialize_available_title


def api(request):
	"""
	JSON contribution from this app.
	"""

	resp = {}

	# Available titles
	available_titles = request.user.kingdom.availabletitle_set.all().select_related("title", "folk")
	resp['available_titles'] = [serialize_available_title(o) for o in available_titles]

	return resp
