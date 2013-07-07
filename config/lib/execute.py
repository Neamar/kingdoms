# -*- coding: utf-8 -*-
"""
Execute some code in a sandboxed environnment
"""
import traceback
import re


def execute(code, param=None, context=None):
	"""
	Runs the specified code, with access to all models.

	param is the param to be used in the script, it will be returned when specified.

	context indicates additional contexts you want to give to the scripter.
	"""

	from kingdom.models import Kingdom, Folk, Message, Claim, ModalMessage
	from internal.models import Constant, FirstName, LastName
	from event.models import Event, PendingEvent
	from mission.models import Mission, PendingMission, PendingMissionAffectation, AvailableMission
	from title.models import Title, AvailableTitle
	from config.scripts.random_scripts import random_in, random_value

	from title.scripts import *
	from event.scripts import *
	from kingdom.scripts import *
	from internal.scripts import *

	from datetime import datetime, timedelta

	_param_specified = param is not None

	status = 'ok'

	# Import context
	if context is not None:
		l = locals()
		for k, v in context.items():
			l[k] = v

	try:
		if code is not None:
			exec(code)
	except Exception as e:
		# Let's try to display something useful fot the scripter team.

		# Retrieve the traceback.
		trace = traceback.format_exc().split("\n")

		# In trace[]
		# -1 is an empty line
		# -2 is the exception
		# -3 is the actual line failing

		# Check the exception was in the script.
		# If not, we'll re raise it, since it is another failure.
		if len(trace) < 3 or not "File \"<string>\"," in trace[-3]:
			# Can't handle that.
			raise

		# Retrieve the exception
		error = trace[-2]

		# Retrieve the number of the failing line of code the script.
		line = int(re.search("([0-9]+)", trace[-3]).group(0))

		# Retrieve from the code the actual line
		code_line = code.split("\n")[line - 1]

		# Format a nice string
		error = "Script error : %s\n%s" % (error, code_line)

		# Replace the default args.
		e.args = (error,)

		# And reraise!
		raise

	if _param_specified:
		return status, param
	else:
		return status
