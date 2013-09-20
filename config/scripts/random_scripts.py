# -*- coding: utf-8 -*-
from random import randint, gauss


def random_in(tab):
	"""
	Return a random value in the specified array.
	"""

	return tab[randint(0, len(tab)-1)]


def random_value(min, max):
	"""
	Return a value between min and max (inclusive).
	"""

	return randint(min, max)


def random_gauss(min, max, mu = None, sigma = None): 
	"""
	Return a random number from a truncated Gaussian distribution.
	"""

	# Compute default μ and σ
	if mu is None:
		mu = (min + max) / 2
	if sigma is None:
		sigma = (min + max) / 6

	for i in range(15):
		x = gauss(mu, sigma) 
		if min <= x <= max: 
			return x
	# With the default mu and sigma, we have 99.7% of chance to find the value in one iteration.
	# Leaving the for loop means miscalculated mu and sigma.
	raise Exception("Bad gaussian parameter values, won't terminate.")


def random_die(max):
	"""
	Returns the results of a die.
	"""

	return randint(1, max)


def fuzzy(max):
	"""
	Returns the results of a die minus another die.
	(Feng-shui style)
	"""

	return random_die(max) - random_die(max)
