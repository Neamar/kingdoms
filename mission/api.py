from mission.models import PendingMission, AvailableMission
from mission.serializers import serialize_folk, serialize_kingdom, serialize_message


def mission_api(request):
	"""
	JSON contribution from this app.
	"""

	resp = {}

	return resp


# Register for execution on /api
from kingdom.views.api import register_object
register_object(mission_api)
