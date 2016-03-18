from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User

class BaseContentTypesModel(models.Model):
	'''
	Abstracte klasse voor modellen die gebruik maken van het contenttypes framework
	'''

	content_type = models.ForeignKey(ContentType, verbose_name='content type', related_name='content_type_set_for_%(class)s')
	object_id = models.PositiveIntegerField(db_index=True) # default name voor GenericForeignKey relaties in contenttypes
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		abstract=True

class Comment(models.Model):
	'''
	Klasse die een comment tekstje van een gebruiker voorstelt, maakt gebruik van contenttypes framework
	'''

	content_type = models.ForeignKey(ContentType, verbose_name='content type', related_name='comment_content_type')
	object_id = models.PositiveIntegerField(db_index=True) # default name voor GenericForeignKey relaties in contenttypes
	content_object = GenericForeignKey('content_type', 'object_id')

	title = models.CharField(max_length=50)
	text = models.CharField(max_length=300)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='comments')

	timestamp = models.DateTimeField(auto_now_add=True, editable=False)


	def __str__(self):
		return "%s 's comment op %s" % (self.user, self.content_object)
