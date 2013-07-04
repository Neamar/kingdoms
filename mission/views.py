
from django.http import Http404
from django.shortcuts import get_object_or_404

from kingdom.decorators import json_view
from mission.models import PendingMission


@json_view
def pending_mission_grid_affect(request, pk, grid_pk):
	"""
	Affect the folk to the mission
	"""
	if not request.method == 'POST':
		raise Http404("Only call this URL by POST.")

	# Retrieve the object
	pending_mission = get_object_or_404(PendingMission, pk=pk, kingdom=request.user.kingdom)

	status = 'ok'
	return {'status': request.POST}
