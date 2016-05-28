from django.contrib import admin
from .models import Vote, Score

# Register your models here.

@admin.register(Vote, Score)


class VoteAdmin(admin.ModelAdmin):
	#fields = ('score', 'user', 'timestamp')
	pass

class ScoreAdmin(admin.ModelAdmin):
	pass