import time
import json
import datetime


class DateTimeEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return int(time.mktime(obj.timetuple()) * 1000)

		return json.JSONEncoder.default(self, obj)


def to_json(dict):
	"""
	Return JSON representation of the dict,
	with date displayed as JS timestamps.
	"""
	return json.dumps(dict, cls=DateTimeEncoder)
