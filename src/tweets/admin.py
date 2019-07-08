# Imports
from django.contrib import admin

# Register your models here.
from .models import Tweet

class TweetModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Tweet

admin.site.register(Tweet, TweetModelAdmin)
