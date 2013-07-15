# -*- coding: utf-8 -*-
"""
Execute some code in a sandboxed environnment
"""

from datetime import datetime, timedelta

from kingdom.models import *
from internal.models import *
from event.models import *
from mission.models import *
from title.models import *

from config.scripts.random_scripts import *
from kingdom.scripts import *
from internal.scripts import *
from title.scripts import *
from event.scripts import *
from mission.scripts import *


def execute(code, param=None, context=None):
	"""
	Runs the specified code, with access to all models.

	param is the param to be used in the script, it will be returned when specified.

	context indicates additional contexts you want to give to the scripter.
	"""

	status = 'ok'

	# Import context
	if context is not None:
		l = locals()
		for k, v in context.items():
			l[k] = v

	if code is not None:
		exec(code)

	return status, param
