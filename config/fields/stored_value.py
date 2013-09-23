import re
import json

from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError


class StoredValueField(models.CharField):
	"""
	Store a value, which can either be a string, an int or a foreign key to some models.
	"""

	description = "A value to be stored"

	__metaclass__ = models.SubfieldBase

	fk_regexp = re.compile("`\w*`:\w*")
	array_regexp = re.compile("^\[.*\]$")
	object_regexp = re.compile("^\{.*\}$")


	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 4096
		kwargs['null'] = True
		super(StoredValueField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		from kingdom.models import Kingdom, Folk, Message, Claim, Quality
		from internal.models import Constant
		from event.models import Event, PendingEvent
		from mission.models import Mission, PendingMission, PendingMissionAffectation
		from title.models import Title, AvailableTitle

		if isinstance(value, (models.Model, list, tuple, dict, QuerySet)):
			return value

		if isinstance(value, basestring) and self.array_regexp.match(value):
			# Array
			return [self.to_python(raw) for raw in json.loads(value)]
		elif isinstance(value, basestring) and self.object_regexp.match(value):
			# Dict
			return {key: self.to_python(v) for key, v in json.loads(value).items()}
		elif isinstance(value, basestring) and self.fk_regexp.match(value):
			# Foreign Key
			class_name, instance_id = value.split(':')
			class_name = class_name[1:-1]
			instance_id = int(instance_id, 10)

			# Instantiate the class from its name
			value_class = locals()[class_name]
		
			try:
				instance = value_class.objects.get(id=instance_id)
				return instance
			except:
				return None
		elif value is None:
			return None
		elif value == "`True`":
			return True
		elif value == "`False`":
			return False
		else:
			try:
				return float(value)
			except ValueError:
				return value
			except TypeError:
				raise ValidationError("Unable to store this data : %s." % value)

	def get_prep_value(self, value):
		if isinstance(value, (list, tuple, QuerySet)):
			return json.dumps([self.get_prep_value(v) for v in value])
		elif isinstance(value, dict):
			return json.dumps({key: self.get_prep_value(v) for key, v in value.items()})
		elif isinstance(value, bool):
			return "`%s`" % str(value)
		if isinstance(value, (int, basestring, float)):
			return value
		elif isinstance(value, models.Model):
			if value.pk is None:
				raise ValidationError("ForeignKey must be saved before being stored.")
			name = value.__class__.__name__
			return '`%s`:%s' % (name, value.pk)
		elif value is None:
			return None
		else:
			raise ValidationError("Value must be int, string or DB object : %s" % value)

	def value_to_string(self, obj):
		value = self._get_val_from_obj(obj)
		return self.get_prep_value(value)


try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^config.fields.stored_value\.StoredValueField'])
except ImportError:
	pass
