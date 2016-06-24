from django.contrib import admin

from .models import Address, Location, Person, FestivalPageRateableAttribute, FestivalPageRatebleAttributeValue, CustomImage,\
	FestivalPageRelatedLink, RelatedLink, FestivalPage#, BlogPage, BlogIndexPage

@admin.register(FestivalPage)
class FestivalPageAdmin(admin.ModelAdmin):
	pass

@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
	pass

@admin.register(BlogIndexPage)
class BlogIndexPageAdmin(admin.ModelAdmin):
	pass

@admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
	pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	pass

'''@admin.register(AddressOrderable)
class AddressOrderableAdmin(admin.ModelAdmin):
	pass'''

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	pass

'''@admin.register(FestivalPagePerson)
class FestivalPagePersonAdmin(admin.ModelAdmin):
	pass'''

@admin.register(FestivalPageRateableAttribute)
class FestivalPageRateableAttributeAdmin(admin.ModelAdmin):
	pass

@admin.register(FestivalPageRatebleAttributeValue)
class FestivalPageRatebleAttributeValueAdmin(admin.ModelAdmin):
	pass

@admin.register(CustomImage)
class FestivalPageCustomImage(admin.ModelAdmin):
	pass

#@admin.register(RelatedLink)
#class RelatedLinkAdmin(admin.ModelAdmin):
#	pass

@admin.register(FestivalPageRelatedLink)
class FestivalPageRelatedLinkAdmin(admin.ModelAdmin):
	pass
