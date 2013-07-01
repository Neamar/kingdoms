from mission.models import PendingMission, AvailableMission
from mission.serializers import serialize_pending_mission


def mission_api(request):
	"""
	JSON contribution from this app.
	"""

	resp = {"hello":True}

	return resp


# Register for execution on /api
from kingdom.views.api import register_object
register_object(mission_api)
