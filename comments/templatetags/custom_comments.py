from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import CommentWithTitle

register = template.Library()


@register.simple_tag
def user_review(user, obj):
	'''
	Deze template retourneert de user review voor een gegeven festival
	Gebruik {% user_review user obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)

	try:
		comment = CommentWithTitle.objects.get(object_pk=obj.pk, content_type=ct, user=user)

	except CommentWithTitle.DoesNotExist:

		return False

	return comment


@register.simple_tag
def user_comment(user, obj):
	'''
	Deze template tag geeft aan of de gebruiker een comment heeft geplaatst voor een gegeven festival

	Gebruik {% user_comment user obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)

	try:
		CommentWithTitle.objects.get(object_pk=obj.pk, content_type=ct, user=user)

	except CommentWithTitle.DoesNotExist:

		return False

	return True


