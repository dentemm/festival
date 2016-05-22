from wagtail.wagtailcore import hooks

from .models import FestivalPageRateableAttribute, FestivalPageRatebleAttributeValue, FestivalPage

@hooks.register('after_edit_page')
def do_after_page_edit(request, page):
	'''
	Nadat een pagina wordt geedit of aangemaakt dienen we na te gaan of 
	er nieuwe Snippet objecten werden aangemaakt
	'''

	# Enkel festival pagina's hebben een update_rating() methode
#	if page.content_type.model_class() == FestivalPage:
#
#		print('tis een festival!!!')
#		page.update_rating()

	#check_snippets(request, page)

	pass



@hooks.register('after_create_page')
def do_after_page_create(request, page):
	'''
	Nadat een pagina wordt geedit of aangemaakt dienen we na te gaan of 
	er nieuwe Snippet objecten werden aangemaakt
	'''

	#check_snippets(request, page)

	pass

def check_snippets(request, page):
	'''
	Als de gebruiker een nieuwe toevoegt, update dan het bijhorende page veld
	'''

	print('nu zijn we hier')


	# -- TEST -- #
	kenmerken = FestivalPageRateableAttribute.objects.all()

	lijst = []

	for kenmerk in kenmerken:

		new, created = FestivalPageRatebleAttributeValue.objects.get_or_create(page=page, rateable_attribute=kenmerk)

		if created == False:
			print('break hier!')
			break

		else:
			lijst.append(new)
			continue

	print('check lengte: %s' % len(page.rateable_attributes.all()))

	page.rateable_attributes = lijst
	page.clean()





