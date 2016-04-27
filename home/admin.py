from django.contrib import admin

from .models import Address, Location, Person, FestivalPageRateableAttribute, FestivalPageRatebleAttributeValue, CustomImage

@admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
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
