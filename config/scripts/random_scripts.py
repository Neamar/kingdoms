from random import randint


def random_between(tab):
	return tab[randint(0, len(tab)-1)]


def random_value(min, max):
	return randint(min, max)