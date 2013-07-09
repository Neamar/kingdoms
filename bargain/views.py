from django.shortcuts import get_object_or_404
from django.http import Http404

from kingdom.decorators import json_view, force_post, status_view
from bargain.models import PendingBargain, PendingBargainKingdom, PendingBargainSharedMission, PendingBargainSharedMissionAffectation
from mission.models import PendingMission, MissionGrid
from kingdom.models import Kingdom, Folk


@force_post
@json_view
@status_view
def pending_bargain_create(request, pk):
	"""
	Create a new pending bargain
	"""

	pending_bargain = PendingBargain()
	pending_bargain.save()

	pending_bargain.pendingbargainkingdom_set.create(kingdom=Kingdom.objects.get(pk=pk))
	pending_bargain.pendingbargainkingdom_set.create(kingdom=request.user.kingdom)


@force_post
@json_view
@status_view
def pending_bargain_delete(request, pk):
	"""
	Delete the pending bargain
	"""

	# Retrieve the objects
	pending_bargain = get_object_or_404(PendingBargain, pk=pk, pendingbargainkingdom__kingdom=request.user.kingdom)

	# Delete
	pending_bargain.delete()


@force_post
@json_view
@status_view
def pending_bargain_share_pending_mission(request, pk):
	"""
	Share a new mission into the bargain.
	"""

	if 'pending_mission' not in request.POST:
		raise Http404("Specify pending_mission in POST")

	# Retrieve the objects
	pending_bargain = get_object_or_404(PendingBargain, pk=pk, pendingbargainkingdom__kingdom=request.user.kingdom)
	pending_mission = get_object_or_404(PendingMission, pk=request.POST['pending_mission'], kingdom=request.user.kingdom)

	# Share the mission
	PendingBargainSharedMission(
		pending_bargain=pending_bargain,
		pending_mission=pending_mission
	).save()


@force_post
@json_view
@status_view
def pending_bargain_kingdom_state(request, pk):
	"""
	Update state for the pending bargain
	"""

	if 'state' not in request.POST:
		raise Http404("Specify state in POST")

	# Retrieve the objects
	pending_bargain_kingdom = get_object_or_404(PendingBargainKingdom, pk=pk, kingdom=request.user.kingdom)

	# Set state
	pending_bargain_kingdom.state = request.POST['state']
	pending_bargain_kingdom.save()


@force_post
@json_view
@status_view
def shared_pending_mission_delete(request, pk):
	"""
	Delete the specified shared pending mission.
	"""

	# Retrieve the objects
	pending_bargain_shared_mission = get_object_or_404(PendingBargainSharedMission, pk=pk, pending_bargain__pendingbargainkingdom__kingdom=request.user.kingdom)

	# Delete
	pending_bargain_shared_mission.delete()


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


@force_post
@json_view
@status_view
def shared_mission_defect(request, pk):
	"""
	Defect the folk from the shared mission
	"""

	# Retrieve the objects
	pending_bargain_shared_mission_affectation = get_object_or_404(PendingBargainSharedMissionAffectation, pk=pk, folk__kingdom=request.user.kingdom)

	# Defect
	pending_bargain_shared_mission_affectation.delete()
