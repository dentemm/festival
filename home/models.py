from __future__ import unicode_literals

from django.db import models as djangomodels
from django.conf import settings

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore import fields
from wagtail.wagtailcore import models
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel, PageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from ratings.models import RatedModelMixin


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

	tags = ClusterTaggableManager(through=FestivalPageTag, blank=True)


	class Meta:
		verbose_name = 'FestivalPagina'


FestivalPage.content_panels = models.Page.content_panels + [
	FieldPanel('name'),
	FieldPanel('description'),
	FieldPanel('descr'),
	InlinePanel('rateable_attributes', label='Te beroordelen eigenschappen')
]

FestivalPage.promote_panels = models.Page.promote_panels + [
	FieldPanel('tags'),
]


class FestivalPageRatebleAttributeValue(djangomodels.Model):
	'''
	Join model for FestivalPage en FestivalAttribute
	'''

	rateable_attribute = djangomodels.ForeignKey('FestivalPageRateableAttribute', related_name='tja')
	page = ParentalKey('home.FestivalPage', related_name='rateable_attributes')

	panels = [
		FieldPanel('rateable_attribute'),
	]

	def __str__(self):

		return self.rateable_attribute.__str__()

@register_snippet
class FestivalPageRateableAttribute(RatedModelMixin, djangomodels.Model):
	'''
	Deze klasse beschrijft een te beoordelen kenmerk van een festival. Het erft van de RatedModelMixin klasse
	twee belangrijke attributen, namelijk get_votes en get_ratings. Daarnaast is er ook de methode get_ratings beschikbaar
	'''

	name = djangomodels.CharField(max_length=27)

	panels = [
		FieldPanel('name'),
	]

	class Meta:
		verbose_name = 'attribute'

	def __str__(self):

		return self.name

@register_snippet
class AddressInformation(djangomodels.Model):
	'''
	'''

	pass
