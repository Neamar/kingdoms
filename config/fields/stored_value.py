import re
import json

from django.db import models
from django.db.models.query import QuerySet
from django.db.models.loading import get_model
from django.core.exceptions import ValidationError
fk_regexp = re.compile("`\w*`:\w*")


class CustomEncoder(json.JSONEncoder):
	"""
	Add some objects as JSON-encodable
	"""
	def default(self, obj):
		if isinstance(obj, models.Model):
			return self.encode_model(obj)
		elif isinstance(obj, QuerySet):
			return self.encode_queryset(obj)

		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, obj)

	def encode_model(self, item):
		if item.pk is None:
			raise ValidationError("ForeignKey must be saved before being stored.")

		return {
			'__t__': 'Model',
			'app': item._meta.app_label,
			'model': item._meta.object_name,
			'pk': item.pk
		}

	def encode_queryset(self, item):
		return list(item)


class CustomDecoder:
	"""
	Add some objects as JSON-decodable
	Warning; does not work intuitively.
	See http://taketwoprogramming.blogspot.fr/2009/06/subclassing-jsonencoder-and-jsondecoder.html
	"""
	def decode(self, d):
		if '__t__' not in d:
			return d

		if d['__t__'] == 'Model':
			return self.decode_model(d)

	def decode_model(self, d):
		model = get_model(d['app'], d['model'])
	
		try:
			return model.objects.get(id=d['pk'])
		except:
			return None
customDecoder = CustomDecoder()


class StoredValueField(models.CharField):
	"""
	Store a value, which can either be a string, an int or a foreign key to some models.
	"""

	description = "A value to be stored"

	__metaclass__ = models.SubfieldBase

	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 4096
		kwargs['null'] = True
		super(StoredValueField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		if isinstance(value, basestring) and value.startswith('JSON:'):
			return json.loads(value[5:], object_hook=customDecoder.decode)
		return value

	def get_prep_value(self, value):
		return 'JSON:' + json.dumps(value, cls=CustomEncoder)

	def value_to_string(self, obj):
		value = self._get_val_from_obj(obj)
		return self.get_prep_value(value)


try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^config.fields.stored_value\.StoredValueField'])
except ImportError:
	pass
