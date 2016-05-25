from .models import FestivalAdvisorUser

def save_profile(backend, user, response, *args, **kwargs):
	'''
	We dienen deze methode toe te voegen aan de default python social auth pipeline
	om een User Profile (= FestivalAdvisorUser) te linken aan de nieuwe gebruiker
	'''

	if kwargs['is_new']:
		print('nieuwe aanmelding!')
		new = FestivalAdvisorUser(user=user)
		new.save()

	else:
		print('geen nieuwe!')
