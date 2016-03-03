from __future__ import unicode_literals

from django.db import models as djangomodels
from django.conf import settings

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore import fields
from wagtail.wagtailcore import models
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from modelcluster.fields import ParentalKey


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


class Comment(djangomodels.Model):

	title = djangomodels.CharField(max_length=63)
	text = djangomodels.CharField(max_length=511)


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

HomePage.content_panels = [
	StreamFieldPanel('body'),
]

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

class FestivalPage(models.Page):


	class Meta:
		verbose_name = 'FestivalPagina'


