# -*- coding: utf-8 -*-
from django.contrib import admin

from title.models import Title, AvailableTitle
from config.lib.admin import DescribedModelAdmin


admin.site.register(Title, DescribedModelAdmin)


class AvailableTitleAdmin(admin.ModelAdmin):
	list_display = ('title', 'kingdom', 'folk')
admin.site.register(AvailableTitle, AvailableTitleAdmin)
