import csv
from decimal import Decimal

from django.apps import apps
from django.views.generic import View, TemplateView, FormView
from django.http import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import formset_factory

from home.models import FestivalPage

from .models import Vote
from .forms import VoteForm, BaseVoteFormSet

# Create your views here.

class FormSetView(TemplateView):

	template_name = 'ratings/ratingform.html'
	

	def post(self, request, *args, **kwargs):

		context = {}

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
	
		rateable_attributes = festival.rateable_attributes.all()
		num_attributes = len(rateable_attributes)

		VoteFormSet = formset_factory(VoteForm, formset=BaseVoteFormSet)

		formset = VoteFormSet(request.POST, request.FILES, instances=rateable_attributes)

		if formset.is_valid():

			for form in formset:
				form.clean()

		number_of_votes = 0
		added_score = 0

		print('formset errors: %s' % formset.errors)

		if formset.is_valid():

			for form in formset:

				score = Decimal(form.cleaned_data['score'])
			

				ct = form.cleaned_data['content_type']
				obj_id = form.cleaned_data['object_id']

				model = apps.get_model(*ct.split(".", 1))
				target = model._default_manager.using(None).get(pk=object_id)

				vote = form.get_vote_object()
				vote.user = request.user

				# Voor elk attribuut: roep Vote.vote() op, wat intern ook een Score object aanmaakt
				# Deze vote() klasse methode zal automatisch ook een db save() operatie uitvoeren
				total_score, num_votes = Vote.vote(ContentType.objects.get_for_model(target), obj_id, request.user, score)

				number_of_votes = num_votes
				added_score += score


			# Nadat alle attributen zijn berekend, kunnen we ook het festival zelf updaten
			fest_ct = ContentType.objects.get_for_model(festival)
			fest_obj_id = festival.pk

			festival_score = added_score / num_attributes

			festival_total, festival_votes = Vote.vote(ContentType.objects.get_for_model(festival), festival.pk, request.user, festival_score)

			context['message'] = 'Bedankt voor je beoordeling!'

		else: 

			context['errors'] = 'Gelieve alle kenmerken een beoordeling te geven!'

		context['formset'] = formset
		context['page'] = festival

		return TemplateResponse(request, self.template_name, context)


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

		#print('form')
		#print(form.cleaned_data)


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


def csvRatings(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="allefestivaladvisorusers.csv"'

	writer = csv.writer(response)


	for fest in FestivalPage.objects.all():

		score = fest.get_ratings()

		if score is not None:

			votes = score.votes

			print(score.num_votes)

			for vote in votes.objects.all():

				print('vote: %s' % vote)


		print('ratings: %s?' % fest.get_ratings())
		#print('votes: %s' % fest.get_votes())



		#votes = fest.rating_votes
		#votes = 'test'
		#score = fest.rating_scores.num_votes
		#print('votes en score: %s -- %s' % (votes, score))

		#writer.writerow([fest.name, user.user.email, user.user.first_name, user.user.last_name])


	return HttpResponse(request)


