from __future__ import unicode_literals

# Django imports
#from django import forms
#from django.contrib import admin
from django.db import models as djangomodels
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Wagtail imports
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore import fields
from wagtail.wagtailcore import models
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel, FieldRowPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

# Third party wagtail dependancies 
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Custom app imports
from ratings.models import RatedModelMixin

# Current app imports
from .managers import UpcomingFestivalManager


# Global StreamField definitions

# 1. Blocks used in StreamField

class ImageWithCaptionBlock(blocks.StructBlock):
	'''
	Dit is een afbeelding met een caption text, kan ook als onderdeel gelden van een carousel
	'''

	image = ImageChooserBlock()
	caption = blocks.TextBlock(required=False)


class HomePageStreamBlock(blocks.StreamBlock):

	carousel = blocks.ListBlock(ImageWithCaptionBlock(), template='home/blocks/carousel.html', icon='image')



class Rating(djangomodels.Model):

	owner = djangomodels.ForeignKey(
		settings.AUTH_USER_MODEL,
		verbose_name='owner',
		null=True,
		blank=True,
		editable=False,
		on_delete=djangomodels.SET_NULL,
		related_name='rated',
		)


class HomePage(models.Page):

	body = fields.StreamField(HomePageStreamBlock(), null=True)

	class Meta:
		verbose_name = 'Startpagina'

HomePage.content_panels = models.Page.content_panels + [

	StreamFieldPanel('body'),
]
#
#
# FESTIVAL INDEX PAGE
#
#
class FestivalIndexPage(models.Page):
	'''
	Deze klasse is een listview van alle opkomende festivals
	'''

	parent_page_types = ['home.FestivalPage']

	@property
	def festivals(self):

		festivals = FestivalPage.objects.live().descendant_of(self)
		festivals = fesetivals.order_by('-date')

		return festivals

	def get_context(self, request):

		festivals = self.festivals

		# pagination
		page = request.GET.get('page')
		paginator = Paginator(festivals, 16)

		try:
			festivals = paginator.page(page)

		except PageNotAnInteger:
			festivals = paginator.page(1)

		except EmptyPage:
			festivals = paginator.page(paginator.num_pages)

		context = super(FestivalIndexPage, self).get_context(request)
		content['festivals'] = festivals

		return context


#
#
# FESTIVAL PAGE 
#
#
class FestivalPageTag(TaggedItemBase):
	'''
	Tags voor FestivalPage
	'''
	content_object = ParentalKey('home.FestivalPage', related_name='tagged_items')

class FestivalPage(models.Page):
	'''
	Deze klasse beschrijft een festival. 
	- Via FestivalPageRateableAttribuut kunnen de te beoordelen aspecten van een festival toegekend worden
	'''

	name = djangomodels.CharField('Festival naam', max_length=40, default='')
	description = djangomodels.TextField(max_length=500, default='')
	descr = fields.RichTextField('Festival promo tekst', blank=True, default='')
	date = djangomodels.DateField('Festival datum', null=True)
	duration = djangomodels.PositiveIntegerField('Duur (# dagen)', default=1)

	location = djangomodels.ForeignKey('Location', related_name='festivals', null=True)
	contact_person = djangomodels.ForeignKey('Person', related_name='festivals', null=True)

	tags = ClusterTaggableManager(through=FestivalPageTag, blank=True)


	upcoming = UpcomingFestivalManager()


	class Meta:
		verbose_name = 'FestivalPagina'
		ordering = ['-date', ]



FestivalPage.content_panels = models.Page.content_panels + [

	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('location', classname='col6'),
				]
			),
			
			FieldRowPanel([
				FieldPanel('date', classname='col6'),
				FieldPanel('duration', classname='col6'),
				],
			),
			FieldPanel('descr'),
			FieldPanel('contact_person'),
		],
		heading='Festival gegevens'
	),


	#FieldPanel('description'),
	
	InlinePanel('rateable_attributes', label='Te beroordelen eigenschappen')
]

FestivalPage.promote_panels = models.Page.promote_panels + [
	FieldPanel('tags'),
]


class FestivalPageRatebleAttributeValue(djangomodels.Model):
	'''
	Join model for FestivalPage en FestivalAttribute
	'''

	rateable_attribute = djangomodels.ForeignKey('FestivalPageRateableAttribute', related_name='+')
	page = ParentalKey('home.FestivalPage', related_name='rateable_attributes')

	panels = [
		FieldPanel('rateable_attribute'),
	]

	def __str__(self):

		return 'kenmerk'

'''
class FestivalPageRateableAttributeValueAdmin(admin.ModelAdmin):

	form = CustomAttributeAdminForm

class CustomAttributeAdminForm(forms.ModelForm):'''





@register_snippet
class FestivalPageRateableAttribute(RatedModelMixin, djangomodels.Model):
	'''
	Deze klasse beschrijft een te beoordelen kenmerk van een festival. Het erft van de RatedModelMixin klasse
	twee belangrijke attributen, namelijk get_votes en get_ratings. Daarnaast is er ook de methode get_ratings beschikbaar
	'''

	name = djangomodels.CharField(max_length=27)

	class Meta:
		verbose_name = 'Beoordeelbaar kenmerk'
		verbose_name_plural = 'Beoordeelbare kenmerken'

	def __str__(self):
		return self.name

FestivalPageRateableAttribute.panels = [
		FieldPanel('name'),
	]

@register_snippet
class Location(djangomodels.Model):

	name = djangomodels.CharField(max_length=28)

	longitude = djangomodels.DecimalField(max_digits=10, decimal_places=7)
	latitude = djangomodels.DecimalField(max_digits=10, decimal_places=7)

	address = djangomodels.ForeignKey('home.Address', related_name='festivals', null=True)

	class Meta:
		verbose_name = 'locatie'
		verbose_name_plural = 'locaties'

	def __str__(self):
		return self.name

Location.panels = [
	FieldPanel('name'),
	FieldPanel('latitude'),
	FieldPanel('longitude'),
	FieldPanel('address')
]


@register_snippet
class Person(djangomodels.Model):

	first_name = djangomodels.CharField(max_length=28)
	last_name = djangomodels.CharField(max_length=64)
	email = djangomodels.EmailField(null=True)
	phone = djangomodels.CharField(max_length=28, null=True)

	class Meta:
		verbose_name = 'persoon'
		verbose_name_plural = 'personen'
		ordering = ['last_name', ]

	def __str__(self):
		return self.first_name + ' ' + self.last_name

@register_snippet
class Address(djangomodels.Model):
	'''
	'''
	
	city = djangomodels.CharField(max_length=40)

	panels = [
		FieldPanel('city'),
	]

	class Meta:
		verbose_name = 'adres'
		verbose_name_plural = 'adressen'

	def __str__(self):
		return self.city
