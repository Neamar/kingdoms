# -*- coding: utf-8 -*-
from django.contrib import admin

from config.admin import ModelAdmin
from title.models import Title, AvailableTitle


class TitleAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'description')
	search_fields = ('name', 'slug', 'description')
admin.site.register(Title, TitleAdmin)


class AvailableTitleAdmin(ModelAdmin):
	list_display = ('title', 'kingdom', 'folk', 'last_folk')
	list_filter = ('title',)
admin.site.register(AvailableTitle, AvailableTitleAdmin)
