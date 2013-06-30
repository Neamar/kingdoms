

def sum_folks(folks, attribute):
	return sum([getattr(folk, attribute) for folk in folks])
