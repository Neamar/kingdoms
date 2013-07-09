from random import randint


def random_in(tab):
	"""
	Return a random value in the specified array.
	"""

	return tab[randint(0, len(tab)-1)]


def random_value(min, max):
	"""
	Return a value between min and max.
	"""

	return randint(min, max)


def random_die(max):
	"""
	Returns the results of a die.
	"""

	return randint(0, max)


def fuzzy(max):
	"""
	Returns the results of a die minus another die.
	(Feng-shui style)
	"""

	return random_die(max) - random_die(max)
