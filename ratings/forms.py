from django import forms
from django.utils.encoding import force_text
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

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

	score = forms.ChoiceField(choices=SELECT_OPTIONS)

	class Meta:
		model = Vote
		fields = ('score', 'content_type', 'object_id' )
		

	def __init__(self, target_object=None, data=None, user=None, score=None, initial=None, **kwargs):
	    self.target_object = target_object

	    print('Vote Form target object = %s' % target_object)

	    if initial is None:
	        initial = {}
	    initial.update(self.generate_meta_data())
	    super(VoteForm, self).__init__(data=data, initial=initial, **kwargs)


	def get_vote_object(self):

		if not self.is_valid():
			raise ValueError('get comment object can only be called on valid forms! -- Tim')

		new = Vote(**self.get_vote_create_data())

		return new

	def generate_meta_data(self):
		'''
		Generate some initial data
		'''

		meta_dict = {}

		if self.target_object:

			meta_dict = {
			    'content_type': str(self.target_object._meta),
			    'object_id': str(self.target_object._get_pk_val()),
			}
		return meta_dict

	def get_vote_create_data(self):

		return dict(
			content_type=ContentType.objects.get_for_model(self.target_object),
			object_id=force_text(self.target_object._get_pk_val())
			)

class BaseVoteFormSet(forms.BaseFormSet):

	def __init__(self, *args, **kwargs):

		self.instances = kwargs.pop('instances')

		super(BaseVoteFormSet, self).__init__(*args, **kwargs)


	def get_form_kwargs(self, index):
		'''
		De get_form_kwargs() methode maakt het mogelijk om init data per form te voorzien
		'''

		kwargs = super(BaseVoteFormSet, self).get_form_kwargs(index)

		#content_type = 

		kwargs['target_object'] = self.instances[index]
		#kwargs['object_id'] = self.instances[index]

		return kwargs


