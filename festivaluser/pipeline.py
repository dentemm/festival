from .models import FestivalAdvisorUser

def save_profile(backend, user, response, *args, **kwargs):
	'''
	We dienen deze methode toe te voegen aan de default python social auth pipeline
	om een User Profile (= FestivalAdvisorUser) te linken aan de nieuwe gebruiker
	'''

	print('--------------------save profile!')

	gender = response.get('gender', '')
	age_range = response.get('age_range', {})
	hometown = response.get('hometown', '')
	age_min = age_range.get('min', 0)
	age_max = age_range.get('max', 100)

	music = response.get('music', 'geen muziek')
	likes = response.get('likes', 'geen likes')
	videos = response.get('videos', 'geen videos')
	tagged_places = response.get('tagged_places', 'geen tagged places')

	print(music)
	print(likes)
	print(videos)
	print(tagged_places)



	print('hometown: %s' % hometown)
	print('args: %s' % str(args))
	print('kwargs: %s' % str(kwargs))

	if kwargs['is_new']:
		#print('nieuwe aanmelding!')
		new = FestivalAdvisorUser(user=user)
		new.gender = gender
		new.age_min = age_min
		new.age_max = age_max
		new.save()

	else:
		#print('geen nieuwe!')
		#print('gender: %s' % gender)

		try: 
			new = FestivalAdvisorUser.objects.get(user=user)

			if new.gender == '':
				new.gender = gender
				new.age_min = age_min
				new.age_max = age_max
				new.save()

		except FestivalAdvisorUser.DoesNotExist:

			new = FestivalAdvisorUser(user=user)
			new.gender = gender
			new.age_min = age_min
			new.age_max = age_max
			new.save()





