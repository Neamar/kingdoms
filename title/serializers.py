def serialize_available_title(available_title):
	"""
	Serialize an available title object to JSON.
	"""

	r = {
		'name': available_title.title.name,
		'description': available_title.title.description,
		'folk': available_title.folk_id
	}

	return r
