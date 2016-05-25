import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from home.models import FestivalPage

# Create your models here.

def get_image_path(instance, filename):
	return os.path.join('users', str(instance.id), filename)

class FestivalAdvisorUser(models.Model):

	#user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loser')
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='festprofile')
	picture = models.ImageField(verbose_name='Profielafbeelding', upload_to=get_image_path, blank=True, null=True)

	favorite_festival = models.ForeignKey(FestivalPage, related_name='+', blank=True, null=True)

	def __str__(self):

		return self.user.username
