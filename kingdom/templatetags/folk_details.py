# -*- coding: utf-8 -*-
from django import template
from django.template import Context, Template
register = template.Library()


@register.filter(name='folk_details')
def folk_details(folk):
	"""
	Display details about a folk
	"""
	raw_context = {
		'folk': folk
	}

	if folk.avatar:
	 raw_context['avatar'] = folk.avatar.image(folk.age())

	template = Template("""
<table>
	<tr>
		<td rowspan="2">
			{% if avatar %}<img src="{{avatar}}" alt="{{folk.last_name}}" alt="Avatar" />{% endif %}
			<span>{{folk.first_name}} {{folk.last_name}}</span>
			<small>( {{folk.age}} ans)</small>
		</td>
		<td><strong>C</strong>{{folk.fight}} </td>
		<td><strong>I</strong>{{folk.plot}} </td>
		<td><strong>D</strong>{{folk.diplomacy}} </td>
		<td><strong>E</strong>{{folk.scholarship}} </td>
		<td><strong>L</strong>{{folk.loyalty}} </td>
	</tr>
	<tr>
		<td colspan="5">
			{% for quality in folk.quality_set.all %}
				{{ quality.name }}
			{% endfor %}
		</td>
	</tr>
</table>
	""")
	return template.render(Context(raw_context))
