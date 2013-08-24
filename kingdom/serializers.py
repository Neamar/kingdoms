from datetime import datetime
from kingdom.scripts import *


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

	def image(folk):
		"""
		Retrieve the URL of an image to display the folk.
		"""
		# Stubs
		if not folk.avatar:
			colors = ("000", "F00", "0F0", "00F", "FF0", "0FF", "FFF", "AAA", "AF0", "A0F", "FA0", "F0A", "0AF", "0FA")
			return "http://placehold.it/100x120/" + colors[folk.pk % len(colors)]

		# Real avatar
		return folk.avatar.image(folk.age())

	r = {
		'id': folk.pk,
		'avatar': image(folk),
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
