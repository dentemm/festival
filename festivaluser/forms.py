from django.models import ModelForm
from .models import FestivalAdvisorUser

class FestivalAdvisorUserForm(ModelForm):

	class Meta:
		model = FestivalAdvisorUser
		fields = ['first_name', 'last_name', 'email', 'picture', 'favorite_festival']