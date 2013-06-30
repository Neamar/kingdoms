"""
Execute some code in a sandboxed environnment
"""


def execute(code, param=None):
	"""
	Runs the specified code, with access to all models.
	"""
	from kingdom.models import Kingdom, Folk, Message, Claim
	from title.models import Constant, Value
	from event.models import Event, EventCategogry, PendingEvent, EventAction
	from mission.models import Mission, MissionGrid, PendingMission, PendingMissionAffectation
	from mission.models import Title, AvailableTitle
	
	_param_specified = param is not None

	status = 'ok'
	exec(code)

	if _param_specified:
		return status, param
	else:
		return status
