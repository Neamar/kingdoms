import re

from django.db import models
from django.core.exceptions import ValidationError


class StoredValueField(models.CharField):
	"""
	Store a value, which can either be a string, an int or a foreign key to some models.
	"""

	description = "A value to be stored"

	__metaclass__ = models.SubfieldBase

	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 512
		kwargs['null'] = True
		super(StoredValueField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		from kingdom.models import Kingdom, Folk, Message, Claim, ModalMessage
		from internal.models import Constant
		from event.models import Event, PendingEvent
		from mission.models import Mission, PendingMission, PendingMissionAffectation
		from title.models import Title, AvailableTitle

		if isinstance(value, models.Model):
			return value

		regexp = re.compile("`\w*`:\w*")

		# Foreign Key
		if isinstance(value, basestring) and regexp.match(value):
			class_name = value.split(':')[0][1:-1]
			instance_id = int(value.split(':')[1], 10)

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
				return int(value)
			except ValueError:
				return value

	def get_prep_value(self, value):
		if isinstance(value, (int, basestring)):
			return value
		elif isinstance(value, bool):
			return "`%s`" % str(value)
		elif isinstance(value, models.Model):
			if value.pk is None:
				raise ValidationError("ForeignKey must be saved before being stored.")
			name = value.__class__.__name__
			return '`%s`:%s' % (name, value.pk)
		elif value is None:
			return None
		else:
			raise ValidationError("Context must be int, string or DB object : %s" % value)

try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^config.fields.stored_value\.StoredValueField'])
except ImportError:
	pass
