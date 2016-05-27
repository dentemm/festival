from django.core import urlresolvers

from . import views

def get_model():

	from .models import CommentWithTitle
	return CommentWithTitle

def get_form():

	from .forms import CommentFormWithTitle
	return CommentFormWithTitle

def get_form_target():

	return '#'