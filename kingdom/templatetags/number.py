# -*- coding: utf-8 -*-
from django import template
register = template.Library()


@register.filter(name='number')
def number(value):
	"""
	Display all letters from the value for small values.
	"""

	numbers = ['zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize']

	if 0 < value < len(numbers):
		return numbers[value]
	else:
		return value

