from wagtail.wagtailcore import hooks

@hooks.register('after_edit_page')
def do_after_page_create(request, page):
  	print('AFTER EDIT PAGE')
  	print(page.contact_person)
  	print(page.persons)

