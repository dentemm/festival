import csv

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, View
from django.core.context_processors import csrf

from .models import FestivalAdvisorUser
from .forms import CustomUserCreationForm

# Create your views here.

def register_user(request):
	'''
	Dit view wordt gebruikt om het aanmeldingsformulier weer te geven, in een modal window
	'''

	if request.user.is_authenticated():

		return HttpResponseRedirect('/user/')

	else:
		if request.method == 'POST':
			form = CustomUserCreationForm(request.POST)	

			if form.is_valid():
				new = form.save()

				#print('user %s' % new)

				username = request.POST['username']
				password = request.POST['password1']

				print('hierzo')
				print(username)
				print(password)

				user = authenticate(username=username, password=password)

				print('user %s' % user)

				if user is not None:
					if user.is_active:
						print('auth login')
						auth_login(request, user)

					else:
						print('not active')

				return HttpResponseRedirect('/user/')

			else:
				print('invalid!!!')
				print(form.errors)

		context = {}
		context.update(csrf(request))
		context['form'] = CustomUserCreationForm()

		#return render(request, 'festivaluser/user_profile.html', context)
		return render(request, 'festivaluser/register_modal.html', context)

def login_user(request):

	if request.method == 'POST':
		form = AuthenticationForm(None, request.POST)

		if form.is_valid():

			auth_login(request, form.get_user())

			print("login gebruiker!")

			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

		else:
			print('invalid!!!')
			print(form)

	context = {}
	context.update(csrf(request))
	context['form'] = AuthenticationForm()

	return render(request, 'festivaluser/login_modal.html', context)


def login(request):
	return render(request, 'login.html')

@login_required(login_url='/')
def account(request):
	return render(request, 'festivaluser/user_profile.html')

def logout(request):
	auth_logout(request)
	return redirect('/')

class LoginView(TemplateView):

	template_name = 'festivaluser/login.html'


class RegistrationView(TemplateView):

	def get(self, request, *args, **kwargs):

		pass

	def post(self, request, *args, **kwargs):

		pass

class UserProfileView(LoginRequiredMixin, TemplateView):

	template_name = 'festivaluser/user_profile.html'

	def get_context_data(self, **kwargs):

		ctx = super(UserProfileView, self).get_context_data(**kwargs)

		if self.request.user.is_authenticated():

			visitor = FestivalAdvisorUser.objects.get(user=self.request.user)
			#print(visitor)
			ctx['visitor'] = visitor

		return ctx

def csvView(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="allefestivaladvisorusers.csv"'

	writer = csv.writer(response)

	all_users = FestivalAdvisorUser.objects.all()

	print(all_users)

	for user in all_users:

		writer.writerow([user.user.username, user.user.email, user.user.first_name, user.user.last_name])
		print('user: %s' % user.user.username)

	return response

