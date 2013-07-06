from django.shortcuts import get_object_or_404

from kingdom.decorators import json_view, force_post, status_view
from bargain.models import PendingBargainSharedMission, PendingBargainSharedMissionAffectation
from mission.models import MissionGrid
from kingdom.models import Folk


@force_post
@json_view
@status_view
def shared_mission_affect(request, pk, grid_pk):
	"""
	Affect the folk to the shared mission
	"""

	if 'folk' not in request.POST:
		raise Http404("Specify folk in POST")

	# Retrieve the objects
	pending_bargain_shared_mission = get_object_or_404(PendingBargainSharedMission, pk=pk, pending_bargain__pendingbargainkingdom__kingdom=request.user.kingdom)
	mission_grid = get_object_or_404(MissionGrid, pk=grid_pk, mission_id=pending_bargain_shared_mission.pending_mission.mission_id)
	folk = get_object_or_404(Folk, pk=request.POST['folk'], kingdom=request.user.kingdom)

	# Affect
	pbsma = PendingBargainSharedMissionAffectation(
		pending_bargain_shared_mission=pending_bargain_shared_mission,
		mission_grid=mission_grid,
		folk=folk
	)

	pbsma.save()
