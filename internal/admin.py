# -*- coding: utf-8 -*-
from django.contrib import admin
from internal.models import Trigger, Constant, Value, Recurring
from kingdom.models import Kingdom


class TriggerAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'prestige_threshold', 'population_threshold')
admin.site.register(Trigger, TriggerAdmin)


class ConstantAdmin (admin.ModelAdmin):
	list_display = ('name', 'value', 'description')
admin.site.register(Constant, ConstantAdmin)


class ValueAdmin(admin.ModelAdmin):
	list_display = ('name', 'kingdom', 'value', 'expiration')
admin.site.register(Value, ValueAdmin)


class RecurringAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'frequency')
	actions = ['resolve']

	def resolve(self, request, queryset):
		kingdoms = Kingdom.objects.all()
		for recurring in queryset:
			for kingdom in kingdoms:
				if recurring.check_condition(kingdom) == "ok":
					recurring.fire(kingdom)
		self.message_user(request, "Les recurrings ont été lancées")
	resolve.short_description = "Do it now"
admin.site.register(Recurring, RecurringAdmin)
