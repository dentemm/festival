from django.db import models
from django.contrib.contenttypes.models import ContentType

class ScoreManager(models.Manager):
	pass

class RatingManager(models.Manager):

	def get_for(self, content_object, **kwargs):
		'''
		Retourneert het Rating object gerelateerd aan het *content_object* en overeenkomstige *kwargs*
		of None wanneer er niet werd gestemd op het object
		'''

		# opmerking: django-generic-ratings gebruikt hiervoor de memoize() functie
		content_type = ContentType.objects.get_for_model(type(content_object))

		try:
			# get() methode van QuerySet API
			return self.get(content_type=content_type, object_id=content_object.pk, **kwargs)

		except self.model.DoesNotExist:
			return None
