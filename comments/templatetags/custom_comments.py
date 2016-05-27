from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import CommentWithTitle

register = template.Library()


@register.simple_tag
def user_comment(user, obj):
	'''
	Deze template tag retourneert de score die een gebruiker heeft uitgebracht op het object

	Gebruik {% user-comment user obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)

	try:
		CommentWithTitle.objects.get(object_pk=obj.pk, content_type=ct, user=user)

	except CommentWithTitle.DoesNotExist:

		return False

	return True


