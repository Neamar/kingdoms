# -*- coding: utf-8 -*-
from datetime import datetime

from django.http import Http404
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404

from kingdom.decorators import json_view, force_post, status_view

from kingdom.models import Kingdom, Folk
from mission.models import PendingMission, PendingMissionAffectation, MissionGrid, AvailableMission


@force_post
@json_view
@status_view
def pending_mission_grid_affect(request, pk, grid_pk):
	"""
	Affect the folk to the mission.
	This function has some additional complexity: it will automatically move someone from a team to a mission.
	"""

	if 'folk' not in request.POST:
		raise Http404("Specify folk in POST")

	# Retrieve the objects
	pending_mission = get_object_or_404(PendingMission, pk=pk, kingdom=request.user.kingdom)
	mission_grid = get_object_or_404(MissionGrid, pk=grid_pk, mission=pending_mission.mission_id)
	folk = get_object_or_404(Folk, pk=request.POST['folk'], kingdom=request.user.kingdom)

	# If the folk is currently in a team, unaffect him
	try:
		if folk.mission.pending_mission.mission.is_team:
			folk.mission.delete()
	except PendingMissionAffectation.DoesNotExist:
		pass

	# Affect
	pma = PendingMissionAffectation(
		pending_mission=pending_mission,
		mission_grid=mission_grid,
		folk=folk
	)

	try:
		sid = transaction.savepoint()
		pma.save()
		transaction.savepoint_commit(sid)
	except IntegrityError:
		transaction.savepoint_rollback(sid)
		raise ValidationError("Cette personne participe déjà à une mission")


@force_post
@json_view
@status_view
def pending_mission_grid_defect(request, pk):
	"""
	Defect the folk from the mission
	"""
	# Retrieve the objects
	pending_mission_affectation = get_object_or_404(PendingMissionAffectation, pk=pk, pending_mission__kingdom=request.user.kingdom)

	# Defect
	pending_mission_affectation.delete()


@force_post
@json_view
@status_view
def pending_mission_set_target(request, pk):
	"""
	Update the target.
	"""

	if 'target' not in request.POST:
		raise Http404("Specify target in POST")

	# Retrieve the objects
	pending_mission = get_object_or_404(PendingMission, pk=pk, kingdom=request.user.kingdom)
	target = get_object_or_404(Kingdom, pk=request.POST['target'])

	# Update target
	pending_mission.target = target
	pending_mission.save()


@force_post
@json_view
@status_view
def pending_mission_set_value(request, pk):
	"""
	Update the value.
	"""

	if 'value' not in request.POST:
		raise Http404("Specify value in POST")

	# Retrieve the objects
	pending_mission = get_object_or_404(PendingMission, pk=pk, kingdom=request.user.kingdom)

	# Update target
	pending_mission.value = request.POST['value']
	pending_mission.save()


@force_post
@json_view
@status_view
def pending_mission_start(request, pk):
	"""
	Start the pending mission
	"""

	# Retrieve the object
	pending_mission = get_object_or_404(PendingMission, pk=pk, kingdom=request.user.kingdom)

	# Start
	pending_mission.started = datetime.now()
	pending_mission.save()


@force_post
@json_view
@status_view
def pending_mission_cancel(request, pk):
	"""
	Cancel the pending mission
	"""

	# Retrieve the object
	pending_mission = get_object_or_404(PendingMission, pk=pk, kingdom=request.user.kingdom)

	# Cancel
	pending_mission.delete()


@force_post
@json_view
@status_view
def available_mission_start(request, pk):
	"""
	Start an available mission.
	"""
	# Retrieve the objects
	available_mission = get_object_or_404(AvailableMission, pk=pk, kingdom=request.user.kingdom)

	# Start the mission
	available_mission.start()
