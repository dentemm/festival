from django.core.management.base import BaseCommand, CommandError

from wagtail.wagtailcore.models import PageRevision

from home.models import FestivalPage

class Command(BaseCommand):

	help = 'Publish all festivals'

	def handle(self, *args, **options):

		revisions = PageRevision.objects.all()

		for item in revisions:

			item.publish()

		self.stdout.write(self.style.SUCCESS('Alles gepubliceerd!'))
