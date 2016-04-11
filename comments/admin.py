from django.contrib import admin
from .models import CommentWithTitle

# Register your models here.
@admin.register(CommentWithTitle)

class CommentWithTitleAdmin(admin.ModelAdmin):
	pass

