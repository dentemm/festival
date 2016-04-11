from django.contrib import admin

from .models import FestivalAdvisorUser

# Register your models here.
@admin.register(FestivalAdvisorUser)

class FestivalAdvisorUserAdmin(admin.ModelAdmin):
	pass

