from django import template
from kingdom.models import Folk
register = template.Library()


@register.filter(name='feminize')
def feminize(folk, arg=None):
	"""
	Feminize a name, according to the gender of the folk.
	"""

	if arg is None:
		arg = ['', 'e']
	else:
		arg = arg.split(',')

	if folk.sex == Folk.MALE:
		return arg[0]
	else:
		return arg[1]
