from django import forms
from django_comments.forms import CommentForm

from .models import CommentWithTitle



class CommentFormWithTitle(CommentForm):

	title = forms.CharField(max_length=60)

	def get_comment_create_data(self):
		# add title field to data
		data = super(CommentFormWithTitle, self).get_comment_create_data()
		data['title'] = self.cleaned_data['title']

		return data

	def get_comment_object(self):

		new = CommentWithTitle(**self.get_comment_create_data())
		new = self.check_for_duplicate_comment(new)

		return new


