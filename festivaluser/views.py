from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, UpdateView
from django.core.context_processors import csrf
from django.contrib.auth.forms import AuthenticationForm


from .models import FestivalAdvisorUser
from .forms import CustomUserCreationForm

def register_user(request):

	if request.user.is_authenticated():

		return HttpResponseRedirect('/user/')

	else:
		if request.method == 'POST':
			form = CustomUserCreationForm(request.POST)	

			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/user/')

			else:
				print('invalid!!!')
				print(form.errors)

		context = {}
		context.update(csrf(request))
		context['form'] = CustomUserCreationForm()

		#return render(request, 'festivaluser/user_profile.html', context)
		return render(request, 'festivaluser/register_modal.html', context)


def ajax_registration(request):

	form = AutenticationForm()

	if request.method == 'POST':

		form = AutenticationForm(None, request.POST)

		if form.is_valid():
			login(request, form.get_user())
			return HttpResponseRedirect()

	return render(request, 'festivaluser/user_profile.html', {'form': form})




# Create your views here.
def login(request):
	return render(request, 'login.html')

@login_required(login_url='/')
def account(request):
	return render(request, 'festivaluser/user_profile.html')

def logout(request):
	auth_logout(request)
	return redirect('/user/login/')

class LoginView(TemplateView):

	template_name = 'festivaluser/login.html'


class RegistrationView(TemplateView):

	def get(self, request, *args, **kwargs):

		pass

	def post(self, request, *args, **kwargs):

		pass

class UserProfileView(TemplateView):

	template_name = 'festivaluser/user_profile.html'

	def get_context_data(self, **kwargs):

		ctx = super(UserProfileView, self).get_context_data(**kwargs)

		if self.request.user.is_authenticated():

			visitor = FestivalAdvisorUser.objects.get(user=self.request.user)
			#print(visitor)
			ctx['visitor'] = visitor

		return ctx
