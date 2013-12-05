# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from kingdom.decorators import json_view, force_post, status_view
from title.models import AvailableTitle
from kingdom.models import Folk


@force_post
@json_view
@status_view
def available_title_affect(request, pk):
	"""
	Affect folk to the title.
	"""

	if 'folk' not in request.POST:
		raise Http404("Specify folk in POST.")

	# Retrieve the objects
	available_title = get_object_or_404(AvailableTitle, pk=pk, kingdom=request.user.kingdom)
	folk = get_object_or_404(Folk, pk=request.POST['folk'], kingdom=request.user.kingdom_id)

	# Save
	available_title.folk = folk

	try:
		available_title.save()
	except IntegrityError:
		raise ValidationError("Cette personne est déjà affectée à un titre.")


@force_post
@json_view
@status_view
def available_title_defect(request, pk):
	"""
	Defect folk from the title.
	"""
	if not request.method == 'POST':
		raise Http404("Only call this URL by POST.")

	# Retrieve the objects
	available_title = get_object_or_404(AvailableTitle, pk=pk, kingdom=request.user.kingdom_id)

	# Save
	available_title.folk = None
	available_title.save()
