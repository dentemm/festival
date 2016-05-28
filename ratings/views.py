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

		print(request)

		self.form = VoteForm()

		return super(TestView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		data = request.POST.copy()

		print(data)

		ctype = data.get("content_type")
		object_id = data.get("object_id")

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