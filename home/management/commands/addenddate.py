from django.core.management.base import BaseCommand, CommandError

from datetime import datetime, timedelta

from home.models import FestivalPage

class Command(BaseCommand):

	help = 'Adss end date for all festivals'

	def handle(self, *args, **options):

		for festival in FestivalPage.objects.all():

			if festival.duration == 0:
				pass

			elif festival.duration == 1:
				pass

			else:
				end_date = festival.date + timedelta(festival.duration)
				festival.end_date = end_date

			festival.save()

		self.stdout.write(self.style.SUCCESS('Het is gefixt!'))

