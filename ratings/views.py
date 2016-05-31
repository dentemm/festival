from django.apps import apps
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import formset_factory


from .models import Vote
from .forms import VoteForm, BaseVoteFormSet

# Create your views here.

class FormSetView(TemplateView):

	template_name = 'ratings/rating.html'

	def post(self, request, *args, **kwargs):

		data = request.POST.copy()

		# 1. reconstruct page
		object_id = data.get('form-0-object_id', 'niks')
		ctype = data.get('form-0-content_type', 'leeg')

		try:
			model = apps.get_model(*ctype.split(".", 1))
			target = model._default_manager.using(None).get(pk=object_id)

		except TypeError:
			return Vote.ObjectDoesNotExist('foutmelding is onjuist, maar tis Tim hier!')

		festival = target.page

		print('attribute %s' % target)
		print('festival %s' % festival)
		print('fest atributes %s' % festival.rateable_attributes.all())

		VoteFormSet = formset_factory(VoteForm, formset=BaseVoteFormSet)

		formset = VoteFormSet(request.POST, request.FILES, instances=festival.rateable_attributes)


		
		#print('data %s' % data)

		

		

		#print('post formset: %s' % formset)

		data = request.POST.copy()


		#print('data %s' % data)

		ctype = data.get("content_type")
		object_id = data.get("object_id")

		if ctype is None or object_id is None:
			return CommentPostBadRequest("Missing content_type or object_pk field.")

		try:
			model = apps.get_model(*ctype.split(".", 1))
			target = model._default_manager.using(None).get(pk=object_id)

		except TypeError:
			return Vote.ObjectDoesNotExist('foutmelding is onjuist, maar tis Tim hier!')



		vote_form = VoteForm(target, data=data)
		vote_formset = VoteFormSet(data)

		if vote_form.is_valid() and vote_formset.is_valid():

			print('tis hier veilig!!!!')




class TestView(TemplateView):

	template_name = 'ratings/rating.html'

	def get(self, request, *args, **kwargs):

		print('form get request %s' % request)

		#VoteFormSet = formset_factory(VoteForm)
		#self.formset = VoteFormSet

		self.form = VoteForm()

		return super(TestView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		data = request.POST.copy()

		print('post form data: %s' % data)

		ctype = data.get("content_type")
		object_id = data.get("object_id")

		if ctype is None or object_id is None:
			return CommentPostBadRequest("Missing content_type or object_pk field.")

		try:
			model = apps.get_model(*ctype.split(".", 1))
			target = model._default_manager.using(None).get(pk=object_id)

		except TypeError:
			return Vote.ObjectDoesNotExist('foutmelding is onjuist, maar tis Tim hier!')

		form = VoteForm(target, data=data)

		if form.errors:
			print('er zijn errors!')


		if form.is_valid():
			score = form.cleaned_data['score']

		print('form')
		print(form.cleaned_data)


		vote = form.get_vote_object()
		vote.user = request.user
		if score:
			vote.score = score

		#vote.save()

		# save() methode wordt voorlopig niet gebruikt, omdat onderstaande klasse methode save() aanroept
		total_score, num_votes = Vote.vote(vote.content_type, object_id, request.user, vote.score)

		data = {
			'user_rating': score,
			'total_score': total_score,
			'num_votes': num_votes, 
		}

		return JsonResponse(data)

	def get_context_data(self, *args, **kwargs):

		ctx = super(TestView, self).get_context_data(*args, **kwargs)

		ctx['form'] = self.form
		#ctx['formset'] = self.form

		return ctx

class RatingView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):

		return super(RatingView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		content_type = get_object_or_404(ContentType, pk=self.kwargs.get('content_type_id'))
		obj = get_object_or_404(content_type.model_class(), pk=self.kwargs.get('object_id'))

		rating_input = int(request.POST.get('rating'))

		# Class method Vote.vote() retourneert de totale score en aantal votes
		total_score, num_votes = Vote.vote(rating=obj, user=request.user, score=rating_input)

		data = {
			'user_rating': rating_input,
			'total_score': total_score,
			'num_votes': num_votes, 
		}

		return JsonResponse(data)