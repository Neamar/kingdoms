# -*- coding: utf-8 -*-
from django import template
from kingdom.models import Folk
register = template.Library()


@register.filter(name='feminize')
def feminize(folk, arg=',e'):
	"""
	Feminize a name, according to the gender of the folk.
	"""

	arg = arg.split(',')

	if folk.sex == Folk.MALE:
		return arg[0]
	else:
		return arg[1]
