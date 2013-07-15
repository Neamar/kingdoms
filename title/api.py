from title.models import AvailableTitle
from title.serializers import serialize_available_title


def api(request):
	"""
	JSON contribution from this app.
	"""

	resp = {}

	# Available titles
	available_titles = AvailableTitle.objects.filter(kingdom=request.user.kingdom).select_related("title", "folk")
	resp['available_titles'] = [serialize_available_title(o) for o in available_titles]

	return resp
