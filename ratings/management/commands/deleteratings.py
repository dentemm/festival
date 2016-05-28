from django.core.management.base import BaseCommand, CommandError

from ratings.models import Vote, Score

class Command(BaseCommand):

	help = 'Verwijder alle Vote en Score objecten'

	def handle(self, *args, **options):

		for vote in Vote.objects.all():

			vote.delete()

		for score in Score.objects.all():

			score.delete()

		self.stdout.write(self.style.SUCCESS('Het is gefixt!'))
