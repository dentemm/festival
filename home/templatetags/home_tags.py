from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import FestivalPageRateableAttribute, FestivalPage, FestivalPageRelatedLink

register = template.Library()


@register.simple_tag
def check_ticket_link(obj):

	print('object: %s' % obj)

	fest = FestivalPage.objects.get(pk=obj)

	for link in obj.related_links.all():

		print('link: %s' % link.title)

		if link.title.lower() == 'tickets':

			#print('jeeeeej')

			return link.link_external

	return ''

@register.simple_tag
def get_festival(object_id, content_type):

	if content_type.model == 'festivalpage':

		return content_type.get_object_for_this_type(pk=object_id)

	return ''


@register.simple_tag
def get_attribute(obj):
	'''
	Deze template tag retourneert h

	Gebruik {% get_attribute <obj> %}
	'''

	name = FestivalPageRateableAttribute.objects.get(pk=obj).__str__()

	return name

