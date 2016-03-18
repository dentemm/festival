from djanog.views.generic import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes import ContentType

from .models import Vote

# Create your views here.

class RatingView(LoginRequiredMixin, View):

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