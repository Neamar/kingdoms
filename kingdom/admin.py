# -*- coding: utf-8 -*-
from django.contrib import admin

from kingdom.models import *
from config.lib.admin import DescribedModelAdmin


class KingdomAdmin(admin.ModelAdmin):
	list_display = ('user', 'prestige', 'population')
admin.site.register(Kingdom, KingdomAdmin)


class FolkAdmin(admin.ModelAdmin):
	list_display = ('name', 'sex')
admin.site.register(Folk, FolkAdmin)


admin.site.register(Quality, DescribedModelAdmin)
admin.site.register(Message)
admin.site.register(ModalMessage)
admin.site.register(Claim)
