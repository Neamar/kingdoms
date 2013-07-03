# -*- coding: utf-8 -*-
from django.contrib import admin

from title.models import Title, AvailableTitle


class TitleAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name', 'description')
admin.site.register(Title, TitleAdmin)


class AvailableTitleAdmin(admin.ModelAdmin):
	list_display = ('title', 'kingdom', 'folk')
	list_filter = ('title',)
admin.site.register(AvailableTitle, AvailableTitleAdmin)
