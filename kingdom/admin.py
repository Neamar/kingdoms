# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from kingdom.models import Kingdom, Folk, Quality, QualityCategory, ModalMessage, Message, Claim
from config.lib.admin import DescribedModelAdmin


class AliveFilter(admin.SimpleListFilter):
	title = _('vivant')
	parameter_name = 'vivant'

	def lookups(self, request, model_admin):
		return (
			('yes', _('Oui')),
			('no', _('Non'))
		)

	def queryset(self, request, queryset):
		if self.value() == 'no':
			return queryset.exclude(death=None)
		else:
			return queryset.filter(death=None)


class KingdomAdmin(admin.ModelAdmin):
	list_display = ('user', 'prestige', 'population', 'money')
admin.site.register(Kingdom, KingdomAdmin)


class EventActionAdminInline(admin.StackedInline):
	model = Quality
	extra = 2


class FolkAdmin(admin.ModelAdmin):
	list_display = ('name', 'sex', 'age')
	list_filter = ('sex', AliveFilter)
admin.site.register(Folk, FolkAdmin)


admin.site.register(QualityCategory, DescribedModelAdmin)


class QualityAdmin(DescribedModelAdmin):
	list_display = ('name', 'category', 'description')
	list_filter = ('category__name',)
admin.site.register(Quality, QualityAdmin)


class MessageAdmin(admin.ModelAdmin):
	list_display = ('kingdom', 'content', 'level', 'read')
admin.site.register(Message, MessageAdmin)


class ModalMessageAdmin(admin.ModelAdmin):
	list_display = ('kingdom', 'name', 'description')
admin.site.register(ModalMessage)


class ClaimAdmin(admin.ModelAdmin):
	list_display = ('offender', 'offended', 'creation')
admin.site.register(Claim)
