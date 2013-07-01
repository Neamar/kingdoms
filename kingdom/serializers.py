def serialize_kingdom(kingdom):
	"""
	Serialize a kingdom object to JSON.
	"""

	r = {
		'population': kingdom.population,
		'prestige': kingdom.prestige,
		'money': kingdom.money
	}

	return r


def serialize_folk(folk):
	"""
	Serialize a folk object to JSON.
	"""
	
	r = {
			'id': folk.id,
			'name': folk.name,
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
			'loyalty': folk.loyalty
	}

	return r


def serialize_message(message):
	"""
	Serialize a message object to JSON.
	"""
	
	r = {
			'content': message.content,
			'level': message.level,
			'read': message.read,
			'creation': message.creation
	}

	return r
