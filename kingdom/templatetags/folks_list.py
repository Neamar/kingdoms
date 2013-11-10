from django import template

register = template.Library()


def _folk_name(folk, first_name_only):
	if first_name_only:
		return folk.first_name
	else:
		return str(folk)


@register.filter(name='folks_list')
def folks_list(folks, arg=''):
	"""
	Display a list of folk : "name1, name2 and name3"
	"""

	first_name_only = (arg == 'short')

	# Convert Queryset to array
	folks = [f for f in folks]

	if len(folks) == 0:
		return ""
	elif len(folks) == 1:
		return _folk_name(folks[0], first_name_only)
	elif len(folks) == 2:
		return _folk_name(folks[0], first_name_only) + " et " + _folk_name(folks[1], first_name_only)
	elif len(folks) > 2:
		return ', '.join([_folk_name(p, first_name_only) for p in folks[0:-1]]) + ' et ' + _folk_name(folks[-1], first_name_only)
