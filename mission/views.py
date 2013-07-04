from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404

from kingdom.decorators import json_view, force_post
from kingdom.models import Folk
from mission.models import PendingMission, PendingMissionAffectation, MissionGrid


@force_post
@json_view
def pending_mission_grid_affect(request, pk, grid_pk):
	"""
	Affect the folk to the mission
	"""

	if 'folk' not in request.POST:
		raise Http404("Specify folk in POST")

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


@force_post
@json_view
def pending_mission_grid_defect(request, pk):
	"""
	Defect the folk from the mission
	"""
	# Retrieve the objects
	pending_mission_affectation = get_object_or_404(PendingMissionAffectation, pk=pk, pending_mission__kingdom=request.user.kingdom)

	# Defect
	pending_mission_affectation.delete()

	status = 'ok'
	return {'status': status}


@json_view
def pending_mission_start(request, pk):
	"""
	Start the pending mission
	"""

	# Retrieve the object
	pending_mission = get_object_or_404(PendingMission, pk=pk, kingdom=request.user.kingdom)

	# Start
	pending_mission.started = datetime.now()
	pending_mission.save()

	status = 'ok'
	return {'status': status}
