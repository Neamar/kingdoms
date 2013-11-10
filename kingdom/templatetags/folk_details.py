# -*- coding: utf-8 -*-
from django import template
from django.template import Context, Template
register = template.Library()


@register.filter(name='folk_details')
def folk_details(folk):
	"""
	Display details about a folk
	"""
	avatar = folk.avatar.image(folk.age())
	template = Template("""
<table>
	<tr>
		<td rowspan="2">
			<img src="{{avatar}}" alt="{{folk.last_name}}" alt="Avatar" />
			<span>{{folk.first_name}} {{folk.last_name}}</span>
			<small>( {{folk.age}}  ans)</small>
		</td>
		<td>{{folk.fight}} <strong>C</strong></td>
		<td>{{folk.plot}} <strong>I</strong></td>
		<td>{{folk.diplomacy}} <strong>D</strong></td>
		<td>{{folk.scholarship}} <strong>É</strong></td>
		<td>{{folk.loyalty}} <strong>L</strong></td>
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
	return template.render(Context({"folk" : folk, 'avatar': avatar}))
