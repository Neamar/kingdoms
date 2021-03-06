from django.db import models
from django import forms
# Source : https://github.com/chrisspen/django-python-code-field


class PythonCodeWidget(forms.Textarea):
	def render(self, name, value, attrs=None):
		"""
		TODO: have a syntax hilight feature, where instead of a TextArea,
		you get a div that can be double-clicked in to make it editable,
		and after leaving it re-highlights.
		"""
		if value is None:
			value = ""
		if attrs is None:
			attrs = {}
		if 'class' in attrs:
			attrs['class'] += " python-code"
		else:
			attrs['class'] = "python-code"
		return super(PythonCodeWidget, self).render(name, value, attrs=attrs)
	
	class Media:
		js = (
			"admin/js/jquery.min.js",
			"code_field/js/codemirror.js",
			"code_field/js/python_field.js",
		)
		css = {
			'all': (
				"code_field/css/line-numbers.css",
			)
		}


class PythonCodeFormField(forms.CharField):
	def __init__(self, *args, **kwargs):
		kwargs['widget'] = PythonCodeWidget
		super(PythonCodeFormField, self).__init__(*args, **kwargs)
	
	def clean(self, value):
		"""
		We need to ensure that the code that was entered validates as
		python code.
		"""
		
		if not value:
			return
		
		if isinstance(value, basestring):
			try:
				value = value.replace('\r', '')
				compile(value, "<string>", 'exec')
			except SyntaxError, arg:
				raise forms.ValidationError(u'Syntax Error: %s' % unicode(arg))
			return value


class ScriptField(models.TextField):
	"""
	A field that will ensure that data that is entered into it is syntactically
	valid python code.
	"""
	
	__metaclass__ = models.SubfieldBase
	description = "Python Source Code"
	
	def formfield(self, **kwargs):
		return super(ScriptField, self).formfield(form_class=PythonCodeFormField, **kwargs)

try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^config\.fields\.script_field\.ScriptField'])
except ImportError:
	pass
