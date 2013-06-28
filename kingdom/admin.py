# -*- coding: utf-8 -*-
from django.contrib import admin

from kingdom.models import Kingdom, Folk, Quality, Message, ModalMessage, Claim


class KingdomAdmin(admin.ModelAdmin):
	list_display = ('user', 'prestige', 'population')
admin.site.register(Kingdom, KingdomAdmin)


class FolkAdmin(admin.ModelAdmin):
	list_display = ('name', 'sex')
admin.site.register(Folk, FolkAdmin)


class QualityAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
admin.site.register(Quality, QualityAdmin)


admin.site.register(Message)
admin.site.register(ModalMessage)
admin.site.register(Claim)
