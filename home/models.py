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


'''
class Comment(djangomodels.Model):

	comment_title = djangomodels.CharField(max_length=63, null=True, blank=True)
	comment_text = djangomodels.CharField(max_length=511, null=True)'''


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
'''
class FestivalPageComment(models.Orderable, djangomodels.Model):

	page = ParentalKey('home.FestivalPage', related_name='festival_comments')
	comment = djangomodels.ForeignKey('home.Comment', related_name='+')

	class Meta:
		verbose_name = 'Festivalpagina comment'
		verbose_name_plural = 'Festivalpagina comments'

	def __str__(self):
		return self.page.title + ' -> ' + self.comment.title

	panels = [
		SnippetChooserPanel('comment')
	]
'''

class FestivalPage(models.Page):

	name = djangomodels.CharField(max_length=40, default='')
	description = djangomodels.TextField(max_length=500, default='')

	attribute = djangomodels.ForeignKey('home.FestivalPageRatebleAttributeValue', null=True, blank=True)

	test_attribute = djangomodels.ForeignKey('home.Test', null=True)

	
	panels = [
		#FieldPanel('name'),
		InlinePanel('home.FestivalPageRateableAttribute', 'rateable_attributes', label='te beoordelen')
	]


	class Meta:
		verbose_name = 'FestivalPagina'


FestivalPage.content_panels = models.Page.content_panels + [
	FieldPanel('name'),
	FieldPanel('description'),
	#FieldPanel('test_attribute')
	SnippetChooserPanel('test_attribute')
	#SnippetChooserPanel('home.FestivalPageRateableAttribute')

	#InlinePanel('home.FestivalPage', 'rateable_attributes', label='te beoordelen')

]



class FestivalPageRatebleAttributeValue(djangomodels.Model):
	'''
	Join model for FestivalPage en FestivalAttribute
	'''

	attribute = djangomodels.ForeignKey('home.FestivalPageRateableAttribute', related_name='attributes')
	page = ParentalKey('home.FestivalPage', related_name='rateable_attributes')

	panels = [
		FieldPanel(attribute),
		PageChooserPanel('page')
	]

@register_snippet
class FestivalPageRateableAttribute(RatedModelMixin, djangomodels.Model):

	page = djangomodels.ForeignKey('home.FestivalPage')
	name = djangomodels.CharField(max_length=27)

	panels = [
		FieldPanel(name),
		PageChooserPanel('page')
	]

	class Meta:
		verbose_name = 'attribute'

@register_snippet
class Test(djangomodels.Model):
	'''
	Eenvoudige FK test
	'''

	name = djangomodels.CharField(max_length=8)

	def __str__(self):
		return self.name

