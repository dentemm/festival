from datetime import datetime

from django.db import models

from wagtail.wagtailcore.models import PageManager


'''
class FestivalPageManager(PageManager):
	pass'''

class UpcomingFestivalManager(PageManager):

	def get_queryset(self):
		return super(UpcomingFestivalManager, self).get_queryset().filter(date__gte=datetime.date.today())


'''
class FestivalPageQuerySet(models.QuerySet):

	def festivals_for_genre(self, genre):
		return self.filter()'''

