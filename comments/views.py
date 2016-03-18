from djanog.views.generic import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes import ContentType

from .models import Comment

# Create your views here.

class RatingView(CommentView, View):

	def post(self, request, *args, **kwargs):

		content_type = get_object_or_404(ContentType, pk=self.kwargs.get('content_type_id'))
		obj = get_object_or_404(content_type.model_class(), pk=self.kwargs.get('object_id'))

		comment_title = request.POST.get('title')
		comment_text = request.POST.get('comment')

		Comment.comment(title=comment_title, comment=comment_text, user=request.user)

		# Class method Vote.vote() retourneert de totale score en aantal votes
		#total_score, num_votes = Vote.vote(rating=obj, user=request.user, score=rating_input)

		data = {
			'comment': comment_text,
			'title': total_score,
		}

		return JsonResponse(data)