

def sum_folks(folks, attribute):
	if attribute == "fight":
		fight_total = 0
		for folk in folks:
			fight_total += folk.fight
		return fight_total
	elif attribute == "diplomacy":
		diplomacy_total = 0
		for folk in folks:
			diplomacy_total += folk.diplomacy
		return diplomacy_total
	elif attribute == "plot":
		plot_total = 0
		for folk in folks:
			plot_total += folk.plot
		return plot_total
	elif attribute == "scholarship":
		scholarship_total = 0
		for folk in folks:
			scholarship_total += 0
		return scholarship_total
	elif attribute == "loyalty":
		loyalty_total = 0
		for folk in folks:
			loyalty_total += folk.loyalty
		return loyalty_total
