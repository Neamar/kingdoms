# -*- coding: utf-8 -*-
"""
Execute some code in a sandboxed environnment
"""
from __future__ import division

from datetime import datetime, timedelta
from django.db.models import Q

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


DEFAULT_STATUS = "ok"

class StopScript(Exception):
	"""
	Class to emulate a "return" in the eval'd code.
	"""
	message = ""

	def __init__(self, message):
		self.message = message
		super(StopScript, self).__init__()


def stop(status=""):
	"""
	Stop script execution right now.
	"""
	raise StopScript(status)


def execute(code, param=None, context=None, filename='<string>'):
	"""
	Runs the specified code, with access to specified context.

	param is the param to be used in the script, it will be returned when specified.

	context indicates additional contexts you want to give to the scripter.

	filename is the name that will be displayed in the stacktrace.
	"""

	status = 'ok'

	# Import context
	if context is not None:
		l = locals()
		for k, v in context.items():
			l[k] = v

	if code is not None:
		try:
			exec(compile(code, filename, 'exec'))
		except StopScript, ss:
			if ss.message != "":
				status = ss.message
			pass

	return status, param
