# -*- coding: utf-8 -*-
"""
Execute some code in a sandboxed environnment
"""


def execute(code, param=None, context=None):
	"""
	Runs the specified code, with access to all models.

	param is the param to be used in the script, it will be returned when specified.

	context indicates additional contexts you want to give to the scripter.
	"""
	from kingdom.models import *
	from title.models import *
	from mission.models import *
	from event.models import *

	_param_specified = param is not None

	status = 'ok'

	# Import context
	if context is not None:
		l = locals()
		for k, v in context.items():
			l[k] = v

	exec(code)

	if _param_specified:
		return status, param
	else:
		return status
