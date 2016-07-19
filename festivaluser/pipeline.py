from .models import FestivalAdvisorUser

def save_profile(backend, user, response, *args, **kwargs):
	'''
	We dienen deze methode toe te voegen aan de default python social auth pipeline
	om een User Profile (= FestivalAdvisorUser) te linken aan de nieuwe gebruiker
	'''

	print('response: %s' % response)

	gender = response.get('gender', '')
	age_range = response.get('age_range', {})
	age_min = age_range.get('min', 0)
	age_max = age_range.get('max', 100)

	#print('args: %s' % str(args))
	#print('kwargs: %s' % str(kwargs))

	if kwargs['is_new']:
		print('nieuwe aanmelding!')
		new = FestivalAdvisorUser(user=user)
		new.gender = gender
		new.age_min = age_min
		new.age_max = age_max
		new.save()

	else:
		print('geen nieuwe!')

		new = FestivalAdvisorUser.objects.get(user=user)

		if new.gender == '':
			new.gender = gender
			new.age_min = age_min
			new.age_max = age_max
			new.save()


