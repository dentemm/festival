from wagtail.wagtailcore import hooks

@hooks.register('after_edit_page')
def do_after_page_edit(request, page):
	'''
	Nadat een pagina wordt geedit of aangemaakt dienen we na te gaan of 
	er nieuwe Snippet objecten werden aangemaakt
	'''

	check_snippets(request, page)



@hooks.register('after_create_page')
def do_after_page_create(request, page):
	'''
	Nadat een pagina wordt geedit of aangemaakt dienen we na te gaan of 
	er nieuwe Snippet objecten werden aangemaakt
	'''

	check_snippets(request, page)

def check_snippets(request, page):
	'''
	Als de gebruiker een nieuwe toevoegt, update dan het bijhorende page veld
	'''

	pass


