from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import FestivalPageRateableAttribute, FestivalPage

register = template.Library()


@register.simple_tag
def get_festival(object_id, content_type):

	if content_type.model == 'festivalpage':

		return content_type.get_object_for_this_type(pk=object_id)

	return ''


@register.simple_tag
def get_attribute(obj):
	'''
	Deze template tag retourneert het totaal aantal gebruikers dat een stem heeft
	uitgebracht op dit object

	Gebruik {% get_attribute <obj> %}
	'''

	name = FestivalPageRateableAttribute.objects.get(pk=obj).__str__()

	return name

