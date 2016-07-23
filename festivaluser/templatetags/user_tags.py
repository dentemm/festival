from datetime import datetime

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

	return count

@register.simple_tag
def user_stats():

	user_dict = {}
	fb_users = 0
	non_fb_users = 0
	total_users = 0
	plus_21_users = 0
	plus_18_users = 0
	plus_13_users = 0
	age_unknown = 0
	male_users = 0
	female_users = 0
	gender_unknown = 0

	for user in FestivalAdvisorUser.objects.all():

		# 1. GENDER CHECK
		if user.gender == 'male':
			male_users += 1

		elif user.gender == 'female':
			female_users += 1

		else:
			gender_unknown += 1

		# 2. AGE CHECK
		if user.age_min == 21:
			plus_21_users += 1

		elif user.age_min == 18:
			plus_18_users += 1

		elif user.age_min == 13:
			plus_13_users += 1

		else:
			age_unknown += 1

		# 3. AUTH CHECK
		if user.user.social_auth.filter(provider='facebook'):

			fb_users += 1

		else:
			non_fb_users += 1

	total_users = fb_users + non_fb_users

	user_dict['fb_users'] = fb_users
	user_dict['non_fb_users'] = non_fb_users
	user_dict['total_users'] = total_users
	user_dict['plus_21_users'] = plus_21_users
	user_dict['plus_18_users'] = plus_18_users
	user_dict['plus_13_users'] = plus_13_users
	user_dict['age_unknown'] = age_unknown
	user_dict['male_users'] = male_users
	user_dict['female_users'] = female_users
	user_dict['gender_unknown'] = gender_unknown

	return user_dict

@register.simple_tag
def last_register():

	last = FestivalAdvisorUser.objects.order_by('user__date_joined').last()
	date = last.user.date_joined.date()

	return date.strftime('%d/%m/%y')




