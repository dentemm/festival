from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, UpdateView

from .models import FestivalAdvisorUser


# Create your views here.
def login(request):
	return render(request, 'login.html')

@login_required(login_url='/')
def account(request):
	return render(request, 'user_profile.html')

def logout(request):
	auth_logout(request)
	return redirect('/')



class UserProfileView(TemplateView):

	template_name = 'user_profile.html'

	def get_context_data(self, **kwargs):

		ctx = super(UserProfileView, self).get_context_data(**kwargs)

		visitor = FestivalAdvisorUser(user=self.request.user)


		ctx['visitor'] = visitor

		return ctx
