from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Score, Vote

register = template.Library()

@register.simple_tag
def votes_count(obj):
	'''
	Deze template tag retourneert het totaal aantal gebruikers dat een stem heeft
	uitgebracht op dit object

	Gebruik {% votes_count <obj> %}
	'''

	count = Vote.objects.filter(
		object_id=obj.pk,
		content_type=ContentType.objects.get_for_model(obj),
	).exclude(overall_rating=0).count()

	return count

@register.simple_tag
def overall_rating(obj):
	'''
	Deze template tag retourneert de overall score van een object

	Gebruik {% overall_rating obj as var %}
	'''

	try:
		ct = ContentType.objects.get_for_model(obj)

		score = Score.objects.get(
			object_id=obj.pk,
			content_type=ct,
		).score or 0

	except Vote.DoesNotExist:
		score = 0

	return score

@register.simple_tag
def user_rating(user, obj):
	'''
	Deze template tag retourneert de score die een gebruiker heeft uitgebracht op het object

	Gebruik {% user-rating user obj %}
	'''

	return user_rating_value(user, obj)

def user_rating_value(user, obj):
	try:
		ct = ContentType.objects.get_for_model(obj)

		score = Vote.objects.get(
			object_id=obj.pk,
			content_type=ct,
			user=user
		).score

	except Vote.DoesNotExist:

		score = 0

	return score