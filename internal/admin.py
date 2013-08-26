# -*- coding: utf-8 -*-
from django.contrib import admin

from internal.models import Trigger, Constant, Recurring, FirstName, LastName, Function, Avatar, Freeze
from kingdom.models import Kingdom


class TriggerAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'prestige_threshold', 'population_threshold')
	search_fields = ('name', 'description')
admin.site.register(Trigger, TriggerAdmin)


class FreezeAdmin(admin.ModelAdmin):
	list_display = ('kingdom', 'created')
	list_filter = ('kingdom',)
	readonly_fields = ('created', 'datas_html')
	exclude = ('datas', 'm2m_datas')
	actions = ['restore',]

	def datas_html(self, obj):
		return '<br /><pre><h3>Datas</h3>\n%s<h3>M2M datas</h3>\n%s</pre>' % (obj.datas, obj.m2m_datas)
	datas_html.short_description = 'Datas'
	datas_html.allow_tags = True

	def restore(self, request, queryset):
		for freeze in queryset:
			freeze.restore()
		self.message_user(request, "Défreezé !")
	restore.short_description = "Défreezer maintenant"

admin.site.register(Freeze, FreezeAdmin)


class ConstantAdmin (admin.ModelAdmin):
	list_display = ('name', 'description', 'value')
	search_fields = ('name', 'description')
	ordering = ('name',)
admin.site.register(Constant, ConstantAdmin)


class FunctionAdmin(admin.ModelAdmin):
	list_display = ('slug', 'description')
	ordering = ('slug',)
admin.site.register(Function, FunctionAdmin)


class RecurringAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'delay')
	search_fields = ('name', 'description')
	ordering = ('name',)
	actions = ['resolve']

	def resolve(self, request, queryset):
		kingdoms = Kingdom.objects.all()
		for recurring in queryset:
			for kingdom in kingdoms:
				if recurring.check_condition(kingdom) == "ok":
					recurring.fire(kingdom)
		self.message_user(request, "Les recurrings ont été lancés")
	resolve.short_description = "Lancer maintenant"
admin.site.register(Recurring, RecurringAdmin)


class FirstNameAdmin(admin.ModelAdmin):
	list_filter = ('sex',)
	list_display = ('name', 'sex')
	search_fields = ('name',)
admin.site.register(FirstName, FirstNameAdmin)


admin.site.register(LastName)


class AvatarAdmin(admin.ModelAdmin):
	list_display = ('sex', 'hair', 'fight', 'thumb_child', 'thumb_adult', 'thumb_old')
	list_display_links = list_display

	def thumb_child(self, obj):
		if obj.child:
			return '<img src="%s" />' % obj.child.url
	thumb_child.allow_tags = True

	def thumb_adult(self, obj):
		if obj.adult:
			return '<img src="%s" />' % obj.adult.url
	thumb_adult.allow_tags = True

	def thumb_old(self, obj):
		if obj.old:
			return '<img src="%s" />' % obj.old.url
	thumb_old.allow_tags = True
admin.site.register(Avatar, AvatarAdmin)

