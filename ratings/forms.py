import time

from django import forms
from django.utils.encoding import force_text
from django.utils import timezone

from .models import Vote


SELECT_OPTIONS = (
	('1', 'slecht'),
	('2', 'matig'),
	('3', 'ok'),
	('4', 'goed'),
	('5', 'top')
)


class VoteForm(forms.Form):

	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.CharField(widget=forms.HiddenInput)

	score = forms.ChoiceField(widget=forms.Select, choices=SELECT_OPTIONS)

	class Meta:
		model = Vote
		fields = ('score', 'content_type', 'object_id' )
		

	def __init__(self, target_object=None, user=None, score=None, initial=None, **kwargs):
	    self.target_object = target_object
	    '''if initial is None:
	        initial = {}
	    initial.update(self.generate_meta_data())'''
	    super(VoteForm, self).__init__(**kwargs)

	def generate_meta_data(self):
		"""Generate some initial data"""

		timestamp = int(time.time())
		security_dict = {
		    'content_type': str(self.target_object._meta),
		    'object_id': str(self.target_object._get_pk_val()),
		}
		return meta_dict



