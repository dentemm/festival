from django.contrib import admin

from .models import Address, Location, AdresOrderable, Person

@admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
	pass

@admin.register(AdresOrderable)
class AdresOrderableAdmin(admin.ModelAdmin):
	pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	pass
