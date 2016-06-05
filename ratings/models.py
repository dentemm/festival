#from datetime import datetime

from django.db import models
from django.db import IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator
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
	score = models.DecimalField(default=0, decimal_places=2, max_digits=4, validators=[MinValueValidator(1), MaxValueValidator(5)]) # Enkel positieve getallen worden ondersteund in deze app

	overall_rating = models.ForeignKey('Score', blank=True, null=True, related_name='votes',)	# foreignkey naar Score, een Score bestaat uit een aantal Votes


	class Meta:
		unique_together = ('content_type', 'object_id', 'user')
		#unique_together = ('content_type', 'object_id', 'user', 'content_object')
		#pass

	def __str__(self):
		return '%s gaf een score van %s op %s' % (self.user, self.score, self.content_object)

	# Huidige implementatie doets niets!
	def save(self, *args, **kwargs):

		return super(Vote, self).save(*args, **kwargs)

	@classmethod
	def vote(cls, rating_object, user, score):
		'''
		De klasse methode vote() voegt een Vote instance toe aan de database, 
		update de gegevens van de Score (of maakt een nieuwe Score instance aan)
		en retourneeert de gegevens total_score en num_votes
		'''
		ct = ContentType.objects.get_for_model(rating_object)

		try: 
			new = cls.objects.create(
				content_type=ct,
				object_id=rating_object.pk,
				user=user,
				score=score
			)

		except IntegrityError:
			print(' - -- - - -- - - - -- tis goed')
			return (0, 0)


		overall_score, is_created = Score.objects.get_or_create(
			object_id=new.pk,
			content_type=ct,
		)


		new.overall_rating = overall_score.update(score) # returns updated score
		new.save()	

		total_score = overall_score.total_score
		num_votes = overall_score.num_votes

		return (total_score, num_votes) #retourneer totale score en aantal stemmen om UI te updaten

	@classmethod
	def vote(cls, ct, object_id, user, score):
		'''
		De klasse methode vote() voegt een Vote instance toe aan de database, 
		update de gegevens van de Score (of maakt een nieuwe Score instance aan)
		en retourneeert de gegevens total_score en num_votes
		'''

		try:
			new = cls.objects.create(
				content_type=ct,
				object_id=object_id,
				user=user,
				score=score
			)

		except IntegrityError:
			print('models.py van ratings app')
			return (0, 0)

		overall_score, is_created = Score.objects.get_or_create(
			object_id=object_id,
			content_type=ct,
		)

		new.overall_rating = overall_score.update(score) # returns updated score
		new.save()	

		total_score = overall_score.total_score
		num_votes = overall_score.num_votes

		return (total_score, num_votes)

class Score(BaseContentTypesModel):
	'''
	De score voor een object wordt bepaald door de uitgebrachte stemmen op dat object. 
	Score.votes is een FK relatie vanuit het Vote model
	'''

	total_score = models.DecimalField(decimal_places=2, max_digits=4, null=True) 	# Optelsom van alle individuele scores
	num_votes = models.PositiveIntegerField(default=0)		# Aantal uitgebrachte stemmen 

	excellent = models.PositiveIntegerField(null=True, blank=True)
	good = models.PositiveIntegerField(null=True, blank=True)
	average = models.PositiveIntegerField(null=True, blank=True)
	bad = models.PositiveIntegerField(null=True, blank=True)

	objects = RatingManager()


	class Meta:
		unique_together = ('content_type', 'object_id', )

	def __str__(self):
		return '%s heeft een score van %s, behaald door %s stemmen' % (self.content_object, self.score, self.num_votes)

	def update(self, score):
		'''
		Deze update() methode wijzigt de total_score en num_votes attributen na uitbrengen van een vote
		'''

		if self.content_type.name == 'Festival':

			self.excellent = 0
			self.good = 0
			self.average = 0
			self.bad = 0

			print('score= %s' % score)

			if score >= 4:
				print('excellent')
				self.excellent += 1

			elif score >= 3:
				print('good')
				self.good += 1

			elif score >= 2:
				print('average')
				self.average += 1

			else:
				print('bad')
				self.bad = 1


		if self.num_votes:
			self.num_votes = self.num_votes + 1

		else:
			self.num_votes = 1

		if self.total_score:
			self.total_score = self.total_score + score

		else:
			self.total_score = score

		self.save()

		return self

	@property
	def score(self):
		score = float(self.total_score/self.num_votes)
		return score

	@property
	def excellent_score(self):

		percentage = str(int(round(100 * self.excellent/self.num_votes))) + '%'

		return percentage

	@property
	def good_score(self):

		percentage = str(int(round(100 * self.good/self.num_votes))) + '%'

		return percentage

	@property
	def average_score(self):

		percentage = str(int(round(100 * self.average/self.num_votes))) + '%'

		return percentage

	@property
	def bad_score(self):

		percentage = str(int(round(100 * self.bad/self.num_votes))) + '%'

		return percentage
	

class RatedModelMixin(models.Model):
	'''
	Deze mixin klasse voegt de rating functionaliteit toe aan het model waarbij je de mixin implementeert
	'''

	rating_scores = GenericRelation(Score)
	rating_votes = GenericRelation(Vote)

	class Meta:
		abstract = True

	def get_ratings(self):

		#print('hmm? %s' % Score.objects.get_for(self))

		return Score.objects.get_for(self)


