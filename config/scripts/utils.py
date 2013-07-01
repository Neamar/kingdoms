

def sum_folks(folks, attribute):
	return sum([getattr(folk, attribute) for folk in folks])


def update_attribute(folks, attribute, value):
	for folk in folks:
		folk.attribute += value
