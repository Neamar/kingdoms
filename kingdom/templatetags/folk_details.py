# -*- coding: utf-8 -*-
from django import template
#from kingdom.models import Folk
from django.template import Context, Template
register = template.Library()


@register.filter(name='folk_details')
def folk_details(folk):
    """
    Display a resume of folk
    """
    template = Template("""
    <table>
        <tr>
            <td rowspan="2">
            <p>
            <img src="{{folk.avatar}}" alt="{{folk.name}}" alt="Avatar" />
                    <span>{{folk.first_name}} {{folk.last_name}}</span>
                    <small>( {{folk.age}}  ans)</small>
                </p>
            </td>
            <td>{{folk.fight}} fight</td>
            <td>{{folk.plot}}  plot</td>
            <td>{{folk.diplomacy}} diplomacy</td>
            <td>{{folk.scholarship}} scholarship</td>
            <td>{{folk.loyalty}} loyalty</td>
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
    return template.render(Context({"folk" : folk}))
