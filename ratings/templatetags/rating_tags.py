from django import template

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

	count = Vote.objects.filter(
		object_id=obj.pk,
		content_type=ContentType.objects.get_for_model(obj),
		).exclude(rating=0).count()

	return count
