from __future__ import unicode_literals

from datetime import datetime, timedelta, date

# Django imports
from django.db import models as djangomodels
from django.db.models.signals import pre_delete
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.template.response import TemplateResponse

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
from wagtail.wagtailadmin.forms import WagtailAdminPageForm, WagtailAdminModelForm
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailsearch import index
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

# Third party wagtail dependancies 
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Other third party dependancies
from django_countries.fields import CountryField

# Custom app imports
from ratings.models import RatedModelMixin
from comments.models import CommentWithTitle

# Current app imports
from .managers import UpcomingFestivalManager, HomePageFeaturedManager
from .forms import  AddressForm
from .custom_panels import CustomInlinePanel

#
#
# FORMS
#
#
class FestivalPageForm(WagtailAdminPageForm):
	'''
	Custom WagtailAdminPageForm subklasse. Deze wordt gebruikt om extra field validation te integreren
	Staat hier omwille van circular import!
	'''

	def test(self):
		pass

	def get_initial(self):

		try: 
			return FestivalPageRateableAttributeValue.objects.get(rateable_attribute=self.initial['name'])

		except:
			return None

	def clean(self):

		page = self.instance

		cleaned_data = super(FestivalPageForm, self).clean()


		if page.id:
			# -- RATEABLE ATTRIBUTES FUNCTIONALITY -- #
			kenmerken = FestivalPageRateableAttribute.objects.all()

			lijst = []

			for kenmerk in kenmerken:

				new, created = FestivalPageRatebleAttributeValue.objects.get_or_create(page=page, rateable_attribute=kenmerk)

				if created == False:
					print('break hier!')
					#lijst = FestivalPageRatebleAttributeValue.objects.all
					break

				else:
					lijst.append(new)
					continue

			if(len(page.rateable_attributes.all()) == 0):
				page.rateable_attributes = lijst

			cleaned_data['rateable_attributes'] = kenmerken

		return cleaned_data

class FestivalPageRateableAttributeValueForm(WagtailAdminModelForm):

	def get_initial(self):

		try: 
			return FestivalPageRateableAttributeValue.objects.get(rateable_attribute=self.initial['name'])

		except:
			return None

#
#
# BLOCK DEFINITIONS
#
#

class TitleBlock(blocks.StructBlock):

	image = ImageChooserBlock(label='afbeelding', required=True)
	title = blocks.CharBlock(label='Titel', required=True)
	auteur = blocks.CharBlock(label='Auteur', required=True)

	class Meta:
		template = 'home/blocks/title_block.html'
		label = 'Blog titel'
		icon = 'title'

class IntroTextBlock(blocks.StructBlock):

	intro = blocks.TextBlock(label='Inleiding van het artikel', required=True)

	class Meta:
		template = 'home/blocks/intro.html'
		label = 'Blog intro'
		icon = 'success'

class SubTitleBlock(blocks.CharBlock):

	class Meta:
		template = 'home/blocks/heading2.html'
		icon = 'bold'
		label = 'Ondertitel'

class VideoBlock(blocks.StructBlock):

	link = EmbedBlock(label='URL van video', required=True, classname='block-background')
	titel = blocks.CharBlock(label='Titel', required=True)
	desc = blocks.CharBlock(label='Beschrijving van video, optioneel', required=False)

	class Meta:
		template = 'home/blocks/video.html'
		icon = 'media'
		label = 'Video'

class GoogleMapBlock(blocks.StructBlock):

	class Meta:
		template = 'home/blocks/google_map.html'
		icon = 'cogs'
		label = 'Google Map'

class Heading1Block(blocks.CharBlock):

	class Meta:
		template = 'home/blocks/heading1.html'
		icon = 'title'
		label = 'Blog titel'

class Heading2Block(blocks.CharBlock):

	class Meta:
		template = 'home/blocks/heading2.html'
		icon = 'bold'
		label = 'Ondertitel'

class PullQuoteBlock(blocks.StructBlock):

	quote = blocks.CharBlock(label='Citaat', required=True, max_length=150, help_text='Geef hier een citaat in')
	person = blocks.CharBlock(label='Auteur', required=True, max_length=28, help_text='Van wie is dit citaat?')

	class Meta:
		template = 'home/blocks/pullquote.html'
		icon = 'openquote'

class ImageWithCaptionBlock(blocks.StructBlock):

	image = ImageChooserBlock()
	text = blocks.CharBlock(required=True, max_length=180, help_text='Geef de afbeelding een korte beschrijving')

	class Meta:
		template = 'home/blocks/image_with_caption.html'
		icon = 'picture'
		label = 'Afbeelding'

#
#
# GLOBAL CLASSES
#
#
class LinkFields(djangomodels.Model):

	link_external = djangomodels.URLField('Externe link', blank=True)
	link_page = djangomodels.ForeignKey(
		'wagtailcore.Page',
		null=True,
		blank=True,
		related_name='+'
	)

	class Meta:
		abstract = True

	@property
	def link(self):

		if self.link_page:
			return self.link_page.url

		else:
			return self.link_external

LinkFields.panels = [
	FieldPanel('link_external'),
]

class RelatedLink(LinkFields):

	title = djangomodels.CharField('titel', max_length=63, help_text='Naam van link')

	class Meta:
		abstract = True

RelatedLink.panels = [
	FieldPanel('title'),
	MultiFieldPanel(LinkFields.panels, 'Link')
]



# Global StreamField definitions

# 1. Blocks used in StreamField


class HomePageStreamBlock(blocks.StreamBlock):

	carousel = blocks.ListBlock(ImageWithCaptionBlock(), template='home/blocks/carousel.html', icon='image')


class HomePage(models.Page):

	template = 'home/home.html'
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
class Location(djangomodels.Model, index.Indexed):
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
		ordering = ['name', ]

	def __str__(self):
		return self.name

Location.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('address', classname='col6')
				]
			),
		],
		heading='Locatie gegevens'
	)
]

Location.search_fields = [
	index.SearchField('name', partial_match=True),
]


@register_snippet
class Address(djangomodels.Model, index.Indexed):
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
		ordering = ['city', ]

	def __str__(self):
		return '%s - %s' % (self.city, self.street)

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

Address.search_fields = [
	index.SearchField('city', partial_match=True),
	index.SearchField('street', partial_match=True),
]

@register_snippet
class Person(ClusterableModel, index.Indexed):
	'''
	Dit model wordt gebruikt om een persoon en zijn contactgegevens te beschrijven
	'''

	page = ParentalKey('home.FestivalPage', related_name='new_person', null=True)

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

Person.search_fields = [
	index.SearchField('first_name', partial_match=True),
]

#@register_snippet
class CommentSnippet(CommentWithTitle):
	'''
	Deze klasse maakt het mogelijk om comments (afkomstig van third party app)
	toe te voegen in de Wagtail admin
	'''
	pass 


#@register_snippet
class FestivalPageRateableAttribute(djangomodels.Model):
	'''
	Deze klasse beschrijft een te beoordelen kenmerk van een festival. Het erft van de RatedModelMixin klasse
	twee belangrijke attributen, namelijk get_votes en get_ratings. Daarnaast is er ook de methode get_ratings beschikbaar
	'''

	name = djangomodels.CharField(max_length=27, unique=True)

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
class FestivalIndexPage(RoutablePageMixin, models.Page):
	'''
	Deze klasse is een listview van alle opkomende festivals. Dit is tevens de homepage
	'''
	template = 'home/home.html'

	@property
	def featured(self):

	    featured =  FestivalPage.upcoming.all()[0:5]
	    return featured

	@property
	def festivals(self):
		'''
		Verkrijg de lijst met festival pagina's die een descendant zijn van deze pagina
		'''

		#festivals = FestivalPage.objects.live().descendant_of(self)
		festivals = FestivalPage.upcoming.all()[5:]
		#festivals = FestivalPage.objects.all()
		#festivals = festivals.order_by('-date')

		return festivals

	@property
	def related_festivals(self):

		related_festivals = FestivalPage.upcoming.all()

		return related_festivals
	

	def get_context(self, request):

		# Featured festivals in homepage
		featured = self.featured

		# Maak gebruik van bovenstaande festivals() functie om alle objecten van FestivalPage queryset te verkrijgen
		festivals = self.festivals

		# pagination
		page = request.GET.get('page', 1)
		paginator = Paginator(festivals, 9)

		try:
			festivals = paginator.page(page)

		except PageNotAnInteger:

			page = request.GET.get('page', 1)
			festivals = paginator.page(1)

		except EmptyPage:
			#festivals = paginator.page(paginator.num_pages)

			festivals = []

		# Update template context
		context = super(FestivalIndexPage, self).get_context(request)
		context['festivals'] = festivals
		context['featured'] = featured

		return context

	@route(r'^$')
	def base(self, request):

		return TemplateResponse(request, template=self.template, context=self.get_context(request))

	@route(r'^test/$')
	def test(self, request):

		template = 'home/home_festival_list.html'

		return TemplateResponse(request, template=template, context=self.get_context(request))	

	@route(r'^related/$')
	def related_festivals(self, request):

		template = 'home/related_festivals.html'
		tag = request.GET.get('tag')

		context = {}

		if tag:

			related_festivals = FestivalPage.upcoming.all()
			related_festivals = related_festivals.filter(tags__name=tag)

			context['related_festivals'] = related_festivals
			context['tag'] = tag

		return TemplateResponse(request, template=template, context=context)

#FestivalPage.parent_page_types = ['home.FestivalIndexPage', ]
FestivalIndexPage.subpage_types = ['home.FestivalPage', 'home.CalendarPage', 'home.BlogIndexPage', ]

#
#
# BLOG PAGE
#
#

class BlogPage(models.Orderable, models.Page):

	template = 'home/blog_page.html'
	date_posted = djangomodels.DateField('Publicatie datum', default=date.today)
	author = djangomodels.CharField('Auteur', max_length=40, null=True)
	#url_title = djangomodels.CharField('URL titel', max_length=40)

	blog_content = fields.StreamField([
		('blog_title', TitleBlock(help_text='Dit is de titel van het artikel, voorzien van een afbeelding')),
		('blogintro', IntroTextBlock(help_text='Hiermee kan je optioneel een korte inleiding voorzien')),
		('subtitle', Heading2Block()),	
		#('video', VideoBlock()),
		('paragraph', blocks.RichTextBlock()),
		('image', ImageWithCaptionBlock()),
		('quote', PullQuoteBlock()),
		#('vid', EmbedBlock()),
	], verbose_name='Blog inhoud')


BlogPage.parent_page_types = ['home.BlogIndexPage', ]
BlogPage.subpage_types = []

BlogPage.content_panels = [
	MultiFieldPanel([
		FieldRowPanel([
				FieldPanel('title', classname='col12'),
				FieldPanel('author', classname='col6'),
				FieldPanel('date_posted', classname='col6'),
			]),
		], heading='Blog informatie',
	),
	StreamFieldPanel('blog_content'),
]

class BlogIndexPage(models.Page):

	template = 'home/blog_index_page.html'

	@property
	def blogs(self):
		# Get list of live blog pages that are descendants of this page
		#blogs = BlogPage.objects.live().descendant_of(self)
		blogs = BlogPage.objects.all()

		# Order by most recent date first
		#blogs = blogs.order_by('-date')

		return blogs

	def get_context(self, request):
		# Get blogs
		blogs = self.blogs

		# Filter by tag
		tag = request.GET.get('tag')
		if tag:
			blogs = blogs.filter(tags__name=tag)

		# Pagination
		page = request.GET.get('page')
		paginator = Paginator(blogs, 10)  # Show 10 blogs per page
		try:
			blogs = paginator.page(page)
		except PageNotAnInteger:
			blogs = paginator.page(1)
		except EmptyPage:
			blogs = paginator.page(paginator.num_pages)

		# Update template context
		context = super(BlogIndexPage, self).get_context(request)
		context['blogs'] = blogs
		return context

BlogIndexPage.subpage_types = ['home.BlogPage', ]
BlogIndexPage.parent_page_types = ['home.FestivalIndexPage', ]

BlogIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
]



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


class FestivalPageRelatedLink(models.Orderable, RelatedLink):
	'''
	Deze klasse wordt gebruikt om interne en externe links aan een festival toe te kennen.
	Dit kunnen links zijn naar gerelateerde festivals, of naar de Facebook account, ticket URL en dergelijk
	'''

	page = ParentalKey('FestivalPage', related_name='related_links')


	def save(self, *args, **kwargs):

		return super(FestivalPageRelatedLink, self).save(*args, **kwargs)


class FestivalPage(RatedModelMixin, models.Page):
	'''
	Deze klasse beschrijft een festival. 
		* Via FestivalPageRateableAttribuut kunnen de te beoordelen aspecten van een festival toegekend worden
	'''
	template = 'home/festival_page.html'

	# Core attributen
	name = djangomodels.CharField('Festival naam', max_length=40, default='', unique=True, 
													help_text='Dit moet een unieke naam zijn!'
													)
	description = fields.RichTextField('Festival promo tekst', 
													help_text='Hier kan je een promo tekstje invullen, al dan niet voorzien van extra tekst styling',
													blank=True, 
													default=''
													)
	date = djangomodels.DateField('Festival datum', null=True)
	duration = djangomodels.PositiveIntegerField('Duur (# dagen)', default=1, validators=[MaxValueValidator(21),])
	end_date = djangomodels.DateField('Eind datum', null=True, blank=True)
	#span_months = djangomodels.BooleanField('Meerdere maanden?', default=False)

	website = djangomodels.URLField(max_length=120, null=True, blank=True, 
													help_text='De link naar de homepage van het festival'
													)
	main_image = djangomodels.ForeignKey('home.CustomImage', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
	pricing = djangomodels.PositiveIntegerField('Prijs (range 0 - 5)', 
													default=0,
													help_text='0 = gratis, 1 = <20€, 2 = <50€, 3 = <100€, 4 = <200€ en 5= >200€', 
													validators=[MaxValueValidator(5), MinValueValidator(0)]
													)

	# Foreign key relaties
	contact_person = djangomodels.ForeignKey('Person', related_name='festivals', null=True, blank=True, on_delete=djangomodels.SET_NULL)
	location = djangomodels.ForeignKey('Location', related_name='festivals', null=True, blank=True, on_delete=djangomodels.SET_NULL)

	tags = ClusterTaggableManager(through=FestivalPageTag, blank=True, 
													help_text=mark_safe('Wordt gebruikt om festivals te filteren, dus het <b><u>genre</u></b> (of genres) zijn ideaal om hier in te geven.')
													)

	# Rating functionality
	#general_rating = djangomodels.DecimalField(default=0, decimal_places=2, max_digits=4)
	#num_votes = djangomodels.PositiveIntegerField(default=0)

	# MODEL MANAGERS
	objects = djangomodels.Manager()		# default manager
	featured = HomePageFeaturedManager()
	upcoming = UpcomingFestivalManager()


	base_form_class = FestivalPageForm

	# PROPERTIES

	@property
	def date_representation(self):

		if self.duration == 0:
			return ''

		else:
			if self.duration == 1:
				return self.date.strftime('%d %B')

			else: 
				end_date = self.date + timedelta(self.duration)

				if self.date.month == end_date.month:
					return '%s - %s %s' % (self.date.strftime('%d'), end_date.strftime('%d'), self.date.strftime('%b'))

				else:
					return '%s - %s' % (self.date.strftime('%d %b'), end_date.strftime('%d %b'))

		return ''
	
	@property
	def check_month_span(self):

		if self.duration == 1:
			return False

		else:
			end_date = self.date + timedelta(self.duration)

			if self.date.month != end_date.month:
				return True

			else:
				return False

		return False

	@property
	def ongoing(self):

		today = datetime.today().date()
		margin = timedelta(days=self.duration)

		return self.date <= today <= self.date + margin


	# METHODS

	def save(self, *args, **kwargs):
		'''
		Deze methode werd overschreven om de title en slug attributes van een Page model in te stellen
		Ze worden ingesteld op basis van de festival naam, en dit bespaart de content editor wat werk
		'''

		# -- MAIN IMAGE FUNCTIONALITY -- #
		main_image = None

		# Als er slechts 1 afbeelding is, dan zal deze steeds primair zijn
		if len(self.images.all()) == 1:

			main = self.images.all()[0]
			main_image = main.image

		# Als er meer dan 1 afbeelding is, zorgen we ervoor dat er slechts 1 primair is
		elif len(self.images.all()) > 1:

			main = self.images.all()[0]
			main_image = main.image


		# Update het main_image attribuut van de bijhorende FestivalPage
		self.main_image = main_image

		# -- END DATE FUNCTIONALITY -- #

		if not self.end_date:

			if self.duration == 0:
				pass

			elif self.duration == 1:
				pass

			else:
				end_date = self.date + timedelta(self.duration)
				self.end_date = end_date


		# -- PAGE TITLE AND PAGE SLUG FUNCTIONALITY -- #

		if self.slug == "" and self.title == "":
			self.title = self.name
			self.slug = slugify(self.name)


		return super(FestivalPage, self).save(*args, **kwargs)

	def update_rating(self, score):

		num_attributes = len(self.rateable_attributes.all())

		score = 0

		for attribute in self.rateable_attributes.all():

			rating = attribute.get_ratings()

			attr_score = rating.score / rating.num_votes


		return 1


	class Meta:
		verbose_name = 'Festival'
		ordering = ['date', ]


# Festival page parent and sub page definition
#FestivalPage.parent_page_types = ['home.FestivalIndexPage', ]
FestivalPage.subpage_types = []

# Festival page panels
FestivalPage.content_panels = [

	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('website', classname='col6'),
				]
			),
			
			FieldRowPanel([
				FieldPanel('date', classname='col6'),
				FieldPanel('duration', classname='col6'),
				],
			),
			FieldRowPanel([
				FieldPanel('pricing', classname='col6'),
				]
			),
			FieldPanel('description'),
			SnippetChooserPanel('contact_person', 'home.Person'),
			SnippetChooserPanel('location', 'home.Location'),
			#FieldPanel('contact_person'),

		],
		heading='Festival gegevens'
	),
	#InlinePanel('rateable_attributes', label='Te beroordelen eigenschappen'),
	InlinePanel('images', label='Festival afbeeldingen'),
	InlinePanel('related_links', 
							label="URL's voor het festival",
							help_text=mark_safe('Bijkomende links voor een festival. Hier kan je ticket links, social media links en andere ingeven. Gebruik best een <b><u>consistente naam</u></b> voor gelijkaardige links, dus niet Facebook voor het ene, en FB voor het andere festival.')
							),
	#InlinePanel('locations', label='festival locaties (hoeft niet ingevuld te worden als er maar 1 locatie is)')
	#InlinePanel('persons', label='Maak nieuwe contactpersoon aan', max_num=1),
	#InlinePanel('rateable_attributes', label='Te beoordelen eigenschappen'),
	#CustomInlinePanel('rateable_attributes', label='Te beoordelen eigenschappen'),
	

]

#FestivalPage.promote_panels = models.Page.promote_panels + [
FestivalPage.promote_panels = [
	FieldPanel('tags'),
]

FestivalPage.search_fields = models.Page.search_fields + (
	index.SearchField('main_image'),
)

#
#
# CALENDAR PAGE
#
#
from django.views.generic.dates import MonthArchiveView

class FestivalMonthArchiveView(MonthArchiveView):
	'''
	Subklasse van MonthArchiveView om paginatie toe te laten volgens maand het festival plaats vindt
	Dit view wordt gebruikt voor CalendarPage
	De get() methode wordt overschreven om per default de huidige maand en het huidige jaar te gebruiken
	'''

	model = FestivalPage
	template_name = 'home/calendar_page.html'

	paginate_by = 75
	context_object_name = 'festival_list'
	date_field = 'date'
	allow_empty = True
	allow_future = True

	def get_context_data(self, **kwargs):

		context = super(FestivalMonthArchiveView, self).get_context_data(**kwargs)

		if self.selected is None:

			all_items = context['object_list']
			current = all_items.last()

			self.selected = current 

		context['selected'] = self.selected

		return context

	def get(self, request, *args, **kwargs):

		selected = request.GET.get('selected', None)

		try:
			festival = FestivalPage.objects.select_related('location').get(pk=selected)
			self.selected = festival

		except FestivalPage.DoesNotExist:
			self.selected = None

		if request.is_ajax():

			template = 'home/festival_content.html'
			context = {}

			if self.selected:
				context['festival'] = self.selected

			return TemplateResponse(request, template=template, context=context)


		# if no date information available: set year and month manually to current year and month
		if request.GET.get('year') == None:

			now = datetime.now()

			self.year = str(now.year)
			self.month = now.strftime("%b")

		return super(FestivalMonthArchiveView, self).get(request, *args, **kwargs)

class CalendarPage(RoutablePageMixin, models.Page):
	'''
	Deze klasse is een listview van alle festivals, en wordt gebruikt om de kalender pagina
	te renderen
	'''

	template = 'home/calendar_page.html'

	#@property
	def festivals(self):
	    
	    festivals = FestivalPage.objects.live()
	    festival = festival.order_by('-date')

	    return festivals


	@route(r'^overview/$', name='monthly')
	def festivals_for_month(self, request):

		return FestivalMonthArchiveView.as_view()(request)


class FestivalPageRatebleAttributeValue(RatedModelMixin, djangomodels.Model):
	'''
	Join model for FestivalPage en FestivalAttribute
	Deze klasse beschrijft een te beoordelen kenmerk van een festival. Het erft van de RatedModelMixin klasse
	twee belangrijke attributen, namelijk get_votes en get_ratings. Daarnaast is er ook de methode get_ratings beschikbaar
	'''

	rateable_attribute = djangomodels.ForeignKey('FestivalPageRateableAttribute', verbose_name='eigenschap', related_name='+')
	page = ParentalKey('home.FestivalPage', related_name='rateable_attributes')
	applicable = djangomodels.BooleanField('van toepassing?', default=True)

	base_form_class = FestivalPageRateableAttributeValueForm


	class Meta:
		unique_together = (
			('page', 'rateable_attribute', ),
		)

	def __str__(self):

		return str(self.rateable_attribute) + ' - ' + str(self.page)

	def save(self, *args, **kwargs):

		return super(FestivalPageRatebleAttributeValue, self).save(*args, **kwargs)



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

	image = djangomodels.ForeignKey(CustomImage, related_name='renditions', db_constraint=False)

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
		verbose_name='afbeelding',
		db_constraint=False
	)
	page = ParentalKey('home.FestivalPage', related_name='images', null=True)
	is_primary = djangomodels.BooleanField('hoofdafbeelding', default=False)

	def __str__(self):
		return 'afbeelding'


	def save(self, *args, **kwargs):
		'''
		Hier wordt nagekeken of er meerdere afbeeldingen zijn met een is_primary flag
		slechts 1 is_primary flag wordt aanvaard, en de main_image attribute van FestivalPage wordt ingesteld
		Opmerking: de save() methode wordt pas opgeroepen tijdens het publiceren van de pagina
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

				for image in self.page.images.all():

					image.is_primary = True
					main_image = self.image
					break

		# Update het main_image attribuut van de bijhorende FestivalPage
		self.page.main_image = main_image
		#self.page.save()

		return super(FestivalImage, self).save(*args, **kwargs)

FestivalImage.panels = [
	MultiFieldPanel([
			ImageChooserPanel('image'),
			FieldPanel('is_primary', classname='title'),
		]
	),
]
