from kingdom.decorators import json_view, force_post, status_view


@force_post
@json_view
@status_view
def freeze_create(request, pk):
	"""
	Create a new freeze for this kingdom.
	"""

	pass


@force_post
@json_view
@status_view
def freeze_restore(request):
	"""
	Restore the last freeze for this kingdom.
	"""

	pass
