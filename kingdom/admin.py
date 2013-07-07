# -*- coding: utf-8 -*-
from django.contrib import admin
from kingdom.models import Kingdom, Folk, Quality, QualityCategory, ModalMessage, Message, Claim


class KingdomAdmin(admin.ModelAdmin):
	list_display = ('user', 'prestige', 'population', 'money')
	search_fields = ('user__username', )
admin.site.register(Kingdom, KingdomAdmin)


class EventActionAdminInline(admin.StackedInline):
	model = Quality
	extra = 2


class FolkAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'kingdom', 'sex', 'birth')
	search_fields = ('first_name', 'last_name')
	list_filter = ('sex', 'kingdom')
admin.site.register(Folk, FolkAdmin)


class QualityCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name', 'description')
admin.site.register(QualityCategory, QualityCategoryAdmin)


class QualityAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'description')
	search_fields = ('name', 'description')
	list_filter = ('category__name',)
admin.site.register(Quality, QualityAdmin)


class MessageAdmin(admin.ModelAdmin):
	list_display = ('kingdom', 'content', 'level', 'read')
admin.site.register(Message, MessageAdmin)


class ModalMessageAdmin(admin.ModelAdmin):
	list_display = ('kingdom', 'name', 'description')
admin.site.register(ModalMessage)


class ClaimAdmin(admin.ModelAdmin):
	list_display = ('offender', 'offended', 'level', 'created')
admin.site.register(Claim, ClaimAdmin)
