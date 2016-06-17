from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock


class GoogleMapBlock(blocks.StructBlock):

	class Meta:
		template = 'home/blocks/google_map.html'
		icon = 'cogs'
		label = 'Google Map'

class PullQuoteBlock(blocks.StructBlock):

	quote = blocks.CharBlock(required=True, max_length=150, help_text='Geef hier een citaat in')
	person = blocks.CharBlock(required=True, max_length=28, help_text='Van wie is dit citaat?')

	class Meta:
		template = 'home/blocks/pullquote.html'
		icon = 'openquote'