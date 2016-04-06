# Django imports
from django.db import models as djangomodels

# Wagtail imports
from wagtail.wagtailcore import models
from wagtail.wagtailcore import fields
from wagtail.wagtailsnippets.models import register_snippet

# Wagtail dependancies
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

#
#
# SNIPPETS
#
#
@register_snippet
class Location(djangomodels.Model):
	'''
	Location object voor festival. Een Location heeft een ForeignKey naar Address
	Longitude en Latitude zijn beschikbaar om locatieweer te geven op een kaart. 
	Een locatie kan een naam hebben, vb Sportpaleis of Schorre
	'''

	name = djangomodels.CharField(max_length=28)
	address = djangomodels.OneToOneField('home.Address', verbose_name='adres', related_name='location', null=True)

	longitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
	latitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

	class Meta:
		verbose_name = 'locatie'
		verbose_name_plural = 'locaties'

	def __str__(self):
		return self.name

	panels = [
		FieldPanel('name'),
		FieldPanel('latitude'),
		FieldPanel('longitude'),
		FieldPanel('address')
	]

@register_snippet
class Address(djangomodels.Model):
	'''
	Address model beschrijft typische adres velden
	'''
	
	city = djangomodels.CharField(verbose_name='stad/gemeente', max_length=40)
	postal_code = djangomodels.CharField(verbose_name='postcode', max_length=8)
	street = djangomodels.CharField(verbose_name='straat', max_length=40)
	number = djangomodels.CharField(verbose_name='nummer', max_length=8)

	panels = [
		FieldPanel('city'),
		FieldPanel('postal_code'),

	]

	class Meta:
		verbose_name = 'adres'
		verbose_name_plural = 'adressen'

	def __str__(self):
		return self.city

#
#
# PAGES
#
#
class FestivalPage(models.Page):
	'''
	Deze klasse beschrijft een festival. 
		* Via FestivalPageRateableAttribuut kunnen de te beoordelen aspecten van een festival toegekend worden
	'''

	name = djangomodels.CharField('Festival naam', max_length=40, default='')
	description = fields.RichTextField('Festival promo tekst', blank=True, default='')
	date = djangomodels.DateField('Festival datum', null=True)
	duration = djangomodels.PositiveIntegerField('Duur (# dagen)', default=1)

	location = djangomodels.ForeignKey('Location', related_name='festivals', null=True, blank=True)
	contact_person = djangomodels.ForeignKey('Person', related_name='festivals', null=True)

	tags = ClusterTaggableManager(through=FestivalPageTag, blank=True)


	class Meta:
		verbose_name = 'FestivalPagina'
		ordering = ['-date', ]



