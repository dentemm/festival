from django.apps import apps
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType


from .models import Vote
from .forms import VoteForm

# Create your views here.

class TestView(TemplateView):

	template_name = 'ratings/rating.html'

	def get(self, request, *args, **kwargs):

		print('form get request %s' % request)

		#print('post form data: %s' % data)

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

		else:
			print('er zijn geen errors!')

		if form.is_valid():
			score = form.cleaned_data['score']

		print('form')
		print(form.cleaned_data)


		vote = form.get_vote_object()
		vote.user = request.user
		if score:
			vote.score = score

		#vote.save()

		total_score, num_votes = Vote.vote(vote.content_type, object_id, request.user, vote.score)

		print('form = %s' % form)
		print('total score: %s -- # votes: %s' % (total_score, num_votes))
		print('ct en id: %s -- %s' % (ctype, object_id))

		return super(TestView, self).post(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):

		ctx = super(TestView, self).get_context_data(*args, **kwargs)

		ctx['form'] = self.form

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