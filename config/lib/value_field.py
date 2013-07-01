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
		super(StoredValueField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		regexp = re.compile("`\w*`:\w*")
		
		if(regexp.match(value)):
			class_name = value.split(':')[0][1:-1]
			instance_id = int(value.split(':')[1], 10)

			# Instantiate the class from its name
			value_class = globals()[class_name]
		
			instance = value_class.objects.get(id=instance_id)
			return instance
		else:
			try:
				return int(value)
			except ValueError:
				return value

	def get_prep_value(self, value):
		if isinstance(value, (int, basestring)):
			return value
		elif isinstance(value, models.Model):
			name = value.__class__.__name__
			return '`%s`:%s' % (name, value.pk)
		else:
			raise ValidationError("Context must be int, string or DB object.")

try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^config.lib\.value_field\.StoredValueField'])
except ImportError:
	pass
