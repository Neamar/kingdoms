import random


def random_between(a, b):
	if random.randint(1, 2) == 1:
		return a
	else:
		return b


def get_random_value(min, max):
	return random.randint(min, max)
