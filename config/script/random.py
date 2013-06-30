import random


def random_sex():
	if random.randint(1, 2) == 1:
		return 'f'
	else:
		return 'm'


def get_random_value(min, max):
	return random.randint(min, max)

