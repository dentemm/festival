from django import template

from ..models import FestivalAdvisorUser

register = template.Library()

@register.simple_tag
def user_count():
	'''
	Deze template tag retourneert het aantal aangemelde gebruikers	
	Gebruik {% user_count %}
	'''

	return FestivalAdvisorUser.objects.count()


@register.simple_tag
def fb_user_count():
	'''
	Deze template tag retourneert het aantal aangemelde gebruikers via facebook
	Gebruik {% fb_user_count %}
	'''

	count = 0

	for user in FestivalAdvisorUser.objects.all():

		if user.user.social_auth.filter(provider='facebook'):
 			count += 1

		else:
			pass

	return count

