# -*- coding: utf-8 -*-
from django import template
register = template.Library()

#du / d'
#le / l'
#que / qu'

@register.filter(name='elide')
def elide(value, args="le,l'"):
	"""
	Elide the value.
	"""

	args = args.split(",")

	if value[0] not in ['a', 'e', 'i', 'o', 'u', 'y']:
		return "%s %s" % (args[0], value)
	else:
		return "%s%s" % (args[1], value)
