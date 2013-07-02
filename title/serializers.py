def serialize_available_title(available_title):
	"""
	Serialize an available title object to JSON.
	"""

	r = {
		'id': available_title.id,
		'title_id': available_title.title_id,
		'name': available_title.title.name,
		'description': available_title.title.description,
		'folk': available_title.folk_id
	}

	return r
