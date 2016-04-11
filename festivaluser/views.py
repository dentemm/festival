from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
	return render(request, 'login.html')

@login_required(login_url='/')
def home(request):
	return render_to_response('home.html')
