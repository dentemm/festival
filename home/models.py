from __future__ import unicode_literals

from django.db import models as djangomodels

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore import fields
from wagtail.wagtailcore import models
from wagtail.wagtailimages.blocks import ImageChooserBlock


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




class HomePage(models.Page):

	body = fields.StreamField(HomePageStreamBlock(), null=True)
