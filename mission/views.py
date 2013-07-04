
from django.http import Http404
from django.shortcuts import get_object_or_404

from kingdom.decorators import json_view
from kingdom.models import Folk
from mission.models import PendingMission, PendingMissionAffectation, MissionGrid


@json_view
def pending_mission_grid_affect(request, pk, grid_pk):
	"""
	Affect the folk to the mission
	"""
	if not request.method == 'POST':
		raise Http404("Only call this URL by POST.")

	if 'folk' not in request.POST:
		raise Http404("Specify folk")

	# Retrieve the objects
	pending_mission = get_object_or_404(PendingMission, pk=pk, kingdom=request.user.kingdom)
	mission_grid = get_object_or_404(MissionGrid, pk=grid_pk, mission=pending_mission.mission_id)
	folk = get_object_or_404(Folk, pk=request.POST['folk'], kingdom=request.user.kingdom)

	# Affect
	pma = PendingMissionAffectation(
		pending_mission=pending_mission,
		mission_grid=mission_grid,
		folk=folk
	)
	pma.save()

	status = 'ok'
	return {'status': status}
