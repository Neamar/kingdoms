# -*- coding: utf-8 -*-
from django.contrib import admin

from kingdom.models import Kingdom, Folk, Quality, QualityCategory, ModalMessage, Message, Claim
from config.lib.admin import DescribedModelAdmin


class KingdomAdmin(admin.ModelAdmin):
	list_display = ('user', 'prestige', 'population', 'money')
admin.site.register(Kingdom, KingdomAdmin)


class EventActionAdminInline(admin.StackedInline):
	model = Quality
	extra = 2


class FolkAdmin(admin.ModelAdmin):
	list_display = ('name', 'sex')
admin.site.register(Folk, FolkAdmin)


admin.site.register(QualityCategory, DescribedModelAdmin)


class FolkAdmin(admin.ModelAdmin):
	list_display = ('name', 'sex')
admin.site.register(Quality, DescribedModelAdmin)


class MessageAdmin(admin.ModelAdmin):
	list_display = ('kingdom', 'content', 'level', 'read')
admin.site.register(Message, MessageAdmin)


class ModalMessageAdmin(admin.ModelAdmin):
	list_display = ('kingdom', 'name', 'description')
admin.site.register(ModalMessage)


class ClaimAdmin(admin.ModelAdmin):
	list_display = ('offender', 'offended', 'creation')
admin.site.register(Claim)
