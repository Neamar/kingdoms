from datetime import datetime


def serialize_kingdom(kingdom):
	"""
	Serialize a kingdom object to JSON.
	"""

	r = {
		'id': kingdom.pk,
		'name': kingdom.user.username,
		'population': kingdom.population,
		'prestige': kingdom.prestige,
		'money': kingdom.money
	}

	return r


def serialize_folk_min(folk):
	"""
	Serialize a folk object to JSON, with minimal information.
	"""

	r = {
		'id': folk.pk,
		'avatar': folk.get_image(),
		'first_name': folk.first_name,
		'last_name': folk.last_name,
	}

	return r


def serialize_folk(folk):
	"""
	Serialize a folk object to JSON.
	"""

	r = {
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
		'age': (datetime.now() - folk.birth).days,
		'raw_qualities': [q.pk for q in folk.quality_set.all()]
	}

	r.update(serialize_folk_min(folk))

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
