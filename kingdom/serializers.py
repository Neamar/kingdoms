def serialize_kingdom(kingdom):
	"""
	Serialize a kingdom object to JSON.
	"""

	r = {
		'id': kingdom.pk,
		'population': kingdom.population,
		'prestige': kingdom.prestige,
		'money': kingdom.money
	}

	return r


colors = ("000", "F00", "0F0", "00F", "FF0", "0FF", "FFF", "AAA")
def serialize_folk(folk):
	"""
	Serialize a folk object to JSON.
	"""

	r = {
		'id': folk.pk,
		'avatar': "http://placehold.it/100x120/" + colors[folk.pk % len(colors)],
		'first_name': folk.first_name,
		'last_name': folk.last_name,
		'mother': folk.mother_id,
		'father': folk.father_id,
		'spouse': folk.spouse_id,
		'mentor': folk.mentor_id,
		'birth': folk.birth,
		'death': folk.death,
		'fight': folk.fight,
		'diplomacy': folk.diplomacy,
		'plot': folk.plot,
		'scholarship': folk.scholarship,
		'loyalty': folk.loyalty,
		'raw_qualities': [q.pk for q in folk.quality_set.all()]
	}

	return r


def serialize_folk_min(folk):
	"""
	Serialize a folk object to JSON, with minimal information.
	"""
	
	r = {
		'id': folk.pk,
		'first_name': folk.first_name,
		'last_name': folk.last_name,
		'avatar': "http://placehold.it/100x120/" + colors[folk.pk % len(colors)],
	}

	return r


def serialize_message(message):
	"""
	Serialize a message object to JSON.
	"""
	
	r = {
		'id': message.pk,
		'content': message.content,
		'level': message.level,
		'read': message.read,
		'created': message.created
	}

	return r


def serialize_quality(quality):
	"""
	Serialize a quality object to JSON.
	"""
	
	r = {
		'id': quality.pk,
		'name': quality.name,
		'description': quality.description
	}

	return r
