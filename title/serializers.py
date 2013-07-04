from django.core.urlresolvers import reverse

from kingdom.serializers import serialize_folk_min


def serialize_available_title(available_title):
	"""
	Serialize an available title object to JSON.
	"""

	r = {
		'id': available_title.id,
		'title_id': available_title.title_id,
		'name': available_title.title.name,
		'description': available_title.title.description,
		'folk': serialize_folk_min(available_title.folk) if available_title.folk is not None else None,
		'links': {
			'affect': reverse('title.views.available_title_affect', args=(available_title.pk,)),
			'defect': reverse('title.views.available_title_defect', args=(available_title.pk,))
		}
	}

	return r
