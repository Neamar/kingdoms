from django.http import Http404
from django.shortcuts import get_object_or_404

from kingdom.decorators import json_view
from title.models import AvailableTitle
from kingdom.models import Folk


@json_view
def available_title_affect(request, pk):
	"""
	Affect folk to the title.
	"""
	if not request.method == 'POST':
		raise Http404("Only call this URL by POST.")

	if 'folk' not in request.POST:
		raise Http404("Specify folk in POST.")

	# Retrieve the objects
	available_title = get_object_or_404(AvailableTitle, pk=pk, kingdom=request.user.kingdom)
	folk = get_object_or_404(Folk, pk=request.POST['folk'], kingdom=request.user.kingdom)

	# Execute code
	#status = available_title.affect(folk)
	print available_title, folk

	return {'status': status}
