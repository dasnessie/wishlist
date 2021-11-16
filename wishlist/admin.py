"""
configures the admin interface
"""
from django.contrib import admin

from .models import Wish


class WishAdmin(admin.ModelAdmin):
    fields = ['bought', 'santa_nick', 'title_text', 'description_text', 'importance', 'link']


admin.site.register(Wish, WishAdmin)
