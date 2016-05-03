import datetime

from django.db import models

from wagtail.wagtailcore.models import PageManager


'''
class FestivalPageManager(PageManager):
	pass'''

class HomePageFeaturedManager(PageManager):

	def get_queryset(self):

		filtered = super(HomePageFeaturedManager, self).get_queryset().filter(date__gte=datetime.date.today())[0:3]

		print('home page featured filter: %s' % str(len(filtered)))

		return super(HomePageFeaturedManager, self).get_queryset().filter(date__gte=datetime.date.today())[0:3]


class UpcomingFestivalManager(PageManager):

	def get_queryset(self):
		return super(UpcomingFestivalManager, self).get_queryset().filter(date__gte=datetime.date.today())


'''
class FestivalPageQuerySet(models.QuerySet):

	def festivals_for_genre(self, genre):
		return self.filter()'''

