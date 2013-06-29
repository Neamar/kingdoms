"""
Execute some code in a sandboxed environnment
"""


def execute(code, param=None):
	"""
	Runs the specified code, with access to all models.
	"""
	from kingdom.models import *
	from title.models import *

	_param_specified = param is not None

	status = 'ok'
	exec(code)

	if _param_specified:
		return status, param
	else:
		return status
