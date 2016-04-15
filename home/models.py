from __future__ import unicode_literals

# Django imports
#from django import forms
#from django.contrib import admin
from django.db import models as djangomodels
from django.db.models.signals import pre_delete
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.dispatch import receiver


# Wagtail imports
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore import fields
from wagtail.wagtailcore import models
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel, FieldRowPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

# Third party wagtail dependancies 
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Other third party dependancies
from django_countries.fields import CountryField
#from recurrence.fields import RecurrenceField

# Custom app imports
from ratings.models import RatedModelMixin
from comments.models import CommentWithTitle


# Current app imports
from .managers import UpcomingFestivalManager
from .forms import FestivalPageForm, AddressForm


#
#
# Global classes
#
#


#@register_snippet
class CommentSnippet(CommentWithTitle):
	'''
	Deze klasse maakt het mogelijk om comments (afkomstig van third party app)
	toe te voegen in de Wagtail admin
	'''
	pass 


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

	template = 'home/home.html'

	body = fields.StreamField(HomePageStreamBlock(), null=True)
	test = fields.RichTextField(blank=True, null=True)


	class Meta:
		verbose_name = _('Startpagina')


HomePage.content_panels = models.Page.content_panels + [

	FieldPanel('test'),
]


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

	name = djangomodels.CharField('locatie naam', max_length=28)
	address = djangomodels.ForeignKey('home.Address', verbose_name='adres', related_name='location', null=True)

	longitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
	latitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

	class Meta:
		verbose_name = 'locatie'
		verbose_name_plural = 'locaties'

	def __str__(self):
		return self.name

Location.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('address', classname='col6')
				]
			),
			FieldRowPanel([
					FieldPanel('latitude', classname='col6'),
					FieldPanel('longitude', classname='col6')
				]
			),
		],
		heading='Locatie gegevens'
	)
]



@register_snippet
class Address(djangomodels.Model):
	'''
	Address model beschrijft typische adres velden
	'''
	
	city = djangomodels.CharField(verbose_name='stad', max_length=40)
	postal_code = djangomodels.CharField(verbose_name='postcode', max_length=8, null=True)
	street = djangomodels.CharField(verbose_name='straat', max_length=40, null=True)
	number = djangomodels.CharField(verbose_name='nummer', max_length=8, null=True)
	country = CountryField(verbose_name='land', null=True, default='BE')

	base_form_class = AddressForm


	class Meta:
		verbose_name = 'adres'
		verbose_name_plural = 'adressen'

	def __str__(self):
		return '%s - %s' % (self.street, self.city)

Address.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('street', classname='col8'),
					FieldPanel('number', classname='col4')
				]
			),
			FieldRowPanel([
					FieldPanel('city', classname='col8'),
					FieldPanel('postal_code', classname='col4')
				]
			),
			FieldRowPanel([
					FieldPanel('country', classname='col6'),
				]
			),
		],
		heading='Persoonsgegevens'
	),
]


@register_snippet
class Person(djangomodels.Model):
	'''
	Dit model wordt gebruikt om een persoon en zijn contactgegevens te beschrijven
	'''

	first_name = djangomodels.CharField('naam', max_length=28, unique=True)
	last_name = djangomodels.CharField('familienaam', max_length=64, blank=True)
	email = djangomodels.EmailField('email adres', null=True, blank=True)
	phone = djangomodels.CharField('telefoon nr', max_length=28, null=True, blank=True)

	class Meta:
		verbose_name = 'persoon'
		verbose_name_plural = 'personen'
		ordering = ['first_name', ]

	def __str__(self):
		return self.first_name + ' ' + self.last_name

	def save(self, *args, **kwargs):

		print('@@@@@ Person class save()')

		return super(Person, self).save(*args, **kwargs)

Person.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('first_name', classname='col6'),
					FieldPanel('last_name', classname='col6')
				]
			),
			FieldRowPanel([
					FieldPanel('email', classname='col6'),
					FieldPanel('phone', classname='col6')
				]
			),
		],
		heading='Persoonsgegevens'
	),
]

'''class FestivalPagePerson(models.Orderable, Person):
	page = ParentalKey('home.FestivalPage', related_name='persons')

	def save(self, *args, **kwargs):

		print('******* festival page person save ')

		print('name: %s' % self.first_name)


		return super(FestivalPagePerson, self).save(*args, **kwargs)'''

#@register_snippet
class FestivalPageRateableAttribute(RatedModelMixin, djangomodels.Model):
	'''
	Deze klasse beschrijft een te beoordelen kenmerk van een festival. Het erft van de RatedModelMixin klasse
	twee belangrijke attributen, namelijk get_votes en get_ratings. Daarnaast is er ook de methode get_ratings beschikbaar
	'''

	name = djangomodels.CharField(max_length=27)

	#base_form_class = MyModelForm

	class Meta:
		verbose_name = 'Beoordeelbaar kenmerk'
		verbose_name_plural = 'Beoordeelbare kenmerken'
		ordering = ['name', ]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):

		return super(FestivalPageRateableAttribute, self).save(*args, **kwargs)

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
	Tags voor FestivalPage, m2m relatie tussen Page en FestivalPageTag wordt voorzien via django-modelcluster
	'''
	content_object = ParentalKey('home.FestivalPage', related_name='tagged_items', null=True)


class FestivalPage(models.Page):
	'''
	Deze klasse beschrijft een festival. 
		* Via FestivalPageRateableAttribuut kunnen de te beoordelen aspecten van een festival toegekend worden
	'''


	name = djangomodels.CharField('Festival naam', max_length=40, default='', unique=True)
	description = fields.RichTextField('Festival promo tekst', blank=True, default='')
	date = djangomodels.DateField('Festival datum', null=True)
	duration = djangomodels.PositiveIntegerField('Duur (# dagen)', default=1)
	website = djangomodels.URLField(max_length=120, null=True, blank=True)
	main_image = djangomodels.ForeignKey(Image, null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
	#test = RecurrenceField(null=True)

	contact_person = djangomodels.ForeignKey('Person', related_name='festivals', null=True, blank=True, on_delete=djangomodels.SET_NULL)
	location = djangomodels.ForeignKey('Location', related_name='festivals', null=True, blank=True)


	tags = ClusterTaggableManager(through=FestivalPageTag, blank=True)

	#upcoming = UpcomingFestivalManager()

	base_form_class = FestivalPageForm

	def save(self, *args, **kwargs):
		'''
		Deze methode werd overschreven om de title en slug attributes van een Page model in te stellen
		Ze worden ingesteld op basis van de festival naam, en dit bespaart de content editor wat werk
		'''

		#test = super(FestivalPage, self).save(*args, **kwargs)


		#print('save page!')
		#print('contact person: %s' % (self.contact_person))


		# If editor has entered a new Person object in the editing interface
		'''if len(self.persons.all()) > 0:

			new = self.persons.all()[0]

			#person, created = Person.objects.get_or_create(first_name=new.first_name, last_name=new.last_name, email=new.email, phone=new.phone)


			print('contact person: %s' % (self.contact_person))
			
			#print('persoon: %s' % new_person)
			self.contact_person = new
			self.contact_person.save()



		self.title = self.name
		self.slug = slugify(self.name)'''


		return super(FestivalPage, self).save(*args, **kwargs)


	class Meta:
		verbose_name = 'Festival'
		ordering = ['-date', ]


# Festival page parent and sub page definition
#FestivalPage.parent_page_types = ['home.FestivalIndexPage', ]
FestivalPage.subpage_types = []

# Festival page panels
FestivalPage.content_panels = [

	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
				]
			),
			
			FieldRowPanel([
				FieldPanel('date', classname='col6'),
				FieldPanel('duration', classname='col6'),
				],
			),
			FieldRowPanel([
				FieldPanel('website', classname='col6'),
				],
			),
			FieldPanel('description'),
			SnippetChooserPanel('contact_person', 'home.Person'),
			SnippetChooserPanel('location', 'home.Location'),
			#FieldPanel('contact_person'),

		],
		heading='Festival gegevens'
	),
	#
	#InlinePanel('rateable_attributes', label='Te beroordelen eigenschappen'),
	InlinePanel('images', label='Festival afbeeldingen'),
	#InlinePanel('persons', label='Maak nieuwe contactpersoon aan', max_num=1),
	#InlinePanel('contact_person', label='test'),

]

#FestivalPage.promote_panels = models.Page.promote_panels + [
FestivalPage.promote_panels = [
	FieldPanel('tags'),
]

class AddressOrderable(models.Orderable, Address):

	page = ParentalKey('home.FestivalPage', related_name='adresorderable')


class OrderableTest(models.Orderable, Location):

	page = ParentalKey('home.FestivalPage', related_name='locaties')
	#name = djangomodels.CharField(max_length=8)
	#test = djangomodels.ForeignKey(Location, null=True)

'''OrderableTest.panels = [
	FieldPanel('name'),
	FieldPanel('test'),
]'''





class FestivalPageRatebleAttributeValue(djangomodels.Model):
	'''
	Join model for FestivalPage en FestivalAttribute
	'''

	rateable_attribute = djangomodels.ForeignKey('FestivalPageRateableAttribute', related_name='+', unique=True)
	page = ParentalKey('home.FestivalPage', related_name='rateable_attributes')

	#base_form_class = MyModelForm


	class Meta:
		pass	
		#unique_together = (
		#	('page', 'rateable_attribute', ),
		#)

	def __str__(self):

		return 'kenmerk'

	def save(self, *args, **kwargs):

		print('SAaaaaaaaaaaava')

		return super(FestivalPageRatebleAttributeValue, self).save(*args, **kwargs)



#FestivalPageRateableAttribute.panels = [
#		FieldPanel('name'),
#]


class FestivalLocation(djangomodels.Model):
	'''
	Through model voor m2m relatie tussen Location en FestivalPage
	'''

	location = djangomodels.ForeignKey('home.Location')
	page = ParentalKey('home.FestivalPage', related_name='locations')

	
FestivalLocation.panels = [
	FieldPanel('location'),
]


#
#
# FESTIVAL PAGE 
#
#

class CustomImage(AbstractImage):
	'''
	Custom image model, om een auteur veld toe te voegen aan de wagtail Images
	'''

	author = djangomodels.CharField('auteur', max_length=56, null=True, blank=True)

	admin_form_fields = Image.admin_form_fields + (

		'author',
	)

class CustomRendition(AbstractRendition):
	'''
	Custom rendition model nodig wanneer je een custom image model toevoegt
	'''

	image = djangomodels.ForeignKey(CustomImage, related_name='renditions')

	class Meta:
		unique_together = (
			('image', 'filter', 'focal_point_key'),
		)

# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=CustomImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)

# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=CustomRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


#@register_snippet
class FestivalImage(djangomodels.Model):
	'''
	Through model voor m2m relatie tussen FestivalPage en wagtailimages.Image
	'''

	image = djangomodels.ForeignKey(
		CustomImage,
		null=True,
		blank=True,
		related_name='+',
		verbose_name='afbeelding'
	)
	page = ParentalKey('home.FestivalPage', related_name='images', null=True)
	is_primary = djangomodels.BooleanField('hoofdafbeelding', default=False)

	def __str__(self):
		return 'afbeelding'


	def save(self, *args, **kwargs):
		'''
		Hier wordt nagekeken of er meerdere afbeeldingen zijn met een is_primary flag
		slecht 1 is_primary flag wordt aanvaard, en de main_image attribute van FestivalPage wordt ingesteld
		'''

		main_image = None

		# Als er slechts 1 afbeelding is, dan zal deze steeds primair zijn
		if len(self.page.images.all()) == 1:

			self.is_primary = True
			main_image = self.image

		# Als er meer dan 1 afbeelding is, zorgen we ervoor dat er slechts 1 primair is
		elif len(self.page.images.all()) > 1:

			primary_present = False

			for image in self.page.images.all():

				if image.is_primary == True and primary_present == False:
					primary_present = True
					main_image = self.image

				else:
					image.is_primary = False

			# Als we uit for loop zijn en nog steeds geen primaire afbeelding, maak dan de eerste primair
			if primary_present == False:

				print('geen enkele!')

				for image in self.page.images.all():

					image.is_primary = True
					main_image = self.image
					break

		# Update het main_image attribuut van de bijhorende FestivalPage
		self.page.main_image = main_image

		return super(FestivalImage, self).save(*args, **kwargs)

FestivalImage.panels = [
	MultiFieldPanel([
			ImageChooserPanel('image'),
			FieldPanel('is_primary', classname='title'),
		]
	),
]
