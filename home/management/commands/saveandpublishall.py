from django.core.management.base import BaseCommand, CommandError

from home.models import FestivalPage

class Command(BaseCommand):

	help = 'Adss end date for all festivals'

	def handle(self, *args, **options):

		for festival in FestivalPage.objects.all():

			latest = festival.get_latest_revision_as_page()

			latest.save_revision().publish()

			#page = festival.save_revision().publish()

		self.stdout.write(self.style.SUCCESS('Alles gepubliceerd'))

