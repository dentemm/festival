#from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User
#from django.utils import timezone

from .managers import RatingManager

# Create your models here.

'''
Deze rating app maakt gebruik van het contenttypes framework van django. We willen immers een stem kunnen 
uitbrengen op verschillende django modellen, dus hebben we generic relations nodig.

Momenteel is de implementatie gebaseerd op: https://github.com/pinax/pinax-ratings/blob/master/pinax/ratings/models.py 
'''


class BaseContentTypesModel(models.Model):
	'''
	Abstracte klasse voor modellen die gebruik maken van het contenttypes framework
	'''

	content_type = models.ForeignKey(ContentType, verbose_name='content type', related_name='content_type_set_for_%(class)s')
	object_id = models.PositiveIntegerField(db_index=True) # default name voor GenericForeignKey relaties in contenttypes
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		abstract=True


class Vote(BaseContentTypesModel):
	'''
	Een Vote object is een stem uitgebracht door een gebruiker op een te beoordelen model. Een gebruiker kan 
	slechts 1 stem uitbrengen op een bepaald model.
	'''

	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='votes')
	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
	score = models.PositiveIntegerField(default=0) # Enkel positieve getallen worden ondersteund in deze app
	#date_changed = models.DateTimeField(default=datetime.now(), editable=False)

	overall_rating = models.ForeignKey('Score', null=True, related_name='votes')	# foreignkey naar Score, een Score bestaat uit een aantal Votes


	class Meta:
		unique_together = ('content_type', 'object_id', 'user')

	def __str__(self):
		return '%s gaf een score van %s op %s' % (self.user, self.score, self.content_object)

	# Huidige implementatie doets niets!
	def save(self, *args, **kwargs):
		#self.date_changed = datetime.now()
		super(Vote, self).save(*args, **kwargs)

	@classmethod
	def vote(cls, rating, user, score):
		ct = ContentType.objects.get_for_model(rating)

		new = cls.objects.create(
			content_type=ct,
			object_id=rating.pk,
			user=user,
			rating=score
		)

		overall_score, is_created = Score.objects.get_or_create(
			object_id=new.pk,
			content_type=ct,
		)

		new.overall_rating = overall_score.update(score) # returns updated score
		new.save()	

		total_score = overall_score.total_score
		num_votes = overall_score.num_votes

		return (total_score, num_votes) #retourneer totale score en aantal stemmen om UI te updaten



class Score(BaseContentTypesModel):
	'''
	De score voor een object wordt bepaald door de uitgebrachte stemmen op dat object. 
	Score.votes is een FK relatie vanuit het Vote model
	'''

	total_score = models.PositiveIntegerField(null=True) 
	num_votes = models.PositiveIntegerField(default=0)

	objects = RatingManager()


	class Meta:
		unique_together = ('content_type', 'object_id', )

	def __str__(self):
		return '%s heeft een score van %s, behaald door %s stemmen' % (self.content_object, self.score, self.votes)

	def update(self, score):

		num_votes = num_votes + 1
		total_score = self.total_score + score
		self.save()

		return self.score

	@property
	def score(self):

		score = float(self.total_score/self.num_votes)

		return score

class RatedModelMixin(models.Model):
	'''
	Deze mixin klasse voegt de rating functionaliteit toe aan het model waarbij je de mixin implementeert
	'''

	rating_scores = GenericRelation(Score)
	rating_votes = GenericRelation(Vote)

	class Meta:
		abstract = True

	def get_ratings(self):

		return Rating.objects.get_for(self)
