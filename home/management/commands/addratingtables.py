from django.core.management.base import BaseCommand, CommandError

from home.models import FestivalPage, FestivalPageRateableAttribute, FestivalPageRatebleAttributeValue

class Command(BaseCommand):

	help = 'Adds latitude and longitude properties for all Address objects'

	def handle(self, *args, **options):

		for page in FestivalPage.objects.all():

			for attribute in FestivalPageRateableAttribute.objects.all():

				new, created = FestivalPageRatebleAttributeValue.objects.get_or_create(page=page, rateable_attribute=attribute)

			if created:
				page.save()

		self.stdout.write(self.style.SUCCESS('Het is gefixt!'))

