from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Score, Vote

register = template.Library()

@register.simple_tag
def rating_count(obj):
	'''
	Deze template tag retourneert het totaal aantal gebruikers dat een stem heeft
	uitgebracht op dit object

	Gebruik {% rating count <obj> %}
	'''

	print('---------- rating count!-----------')
	print('pk: ' + str(obj.pk))
	print('ct: ' + str(ContentType.objects.get_for_model(obj)))

	count = Vote.objects.filter(
		object_id=obj.pk,
		content_type=ContentType.objects.get_for_model(obj),
		).exclude(rating=0).count()

	return count
