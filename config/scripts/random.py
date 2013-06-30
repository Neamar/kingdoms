import random


def random_between(tab):
	return tab[random.randint(0, len(tab)-1)]


def random_value(min, max):
	return random.randint(min, max)
