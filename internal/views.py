from kingdom.decorators import json_view, force_post, status_view


@force_post
@json_view
@status_view
def freeze_create(request):
	"""
	Create a new freeze for this kingdom.
	"""

	request.user.kingdom.freeze_set.create()


@force_post
@json_view
@status_view
def freeze_restore(request):
	"""
	Restore the last freeze for this kingdom, and delete it.
	"""

	freeze = request.user.kingdom.freeze_set.order_by('-created')[0]
	freeze.restore()
	freeze.delete()
