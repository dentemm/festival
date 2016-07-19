from django.db import models
from django_comments.models import CommentAbstractModel

# Create your models here.
class CommentWithTitle(CommentAbstractModel):
	'''
	Een uitbreiding van django_comments.models.Comment om naast tekst ook een titel te kunnen voorzien.
	Deze titel wordt gebruikt doorheen de website als een samenvatting van een comment
	'''

	title = models.CharField(max_length=60)

	class Meta:

		unique_together = ('content_type', 'object_pk', 'user')
		verbose_name = 'commentaar'
		verbose_name_plural = 'User comments'
