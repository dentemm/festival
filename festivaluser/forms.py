from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import FestivalAdvisorUser

class FestivalAdvisorUserForm(ModelForm):

	class Meta:
		model = FestivalAdvisorUser
		fields = ['picture', 'favorite_festival']

class CustomUserCreationForm(UserCreationForm):

	email = forms.EmailField(required=True)

	class Meta:

		model = User
		fields = UserCreationForm.Meta.fields + ('email',)

	def save(self, commit=True):
		user = super(CustomUserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		# Maak een nieuwe FestivalAdvisorUser aan met de zonet aangemaakte User
		new = FestivalAdvisorUser(user)
		new.save()

		if commit:
			user.save()

		return user