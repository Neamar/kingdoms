# -*- coding: utf-8 -*-
from django.contrib import admin
from internal.models import Trigger, Constant, Value, Recurring, FirstName, LastName, Function, Avatar
from kingdom.models import Kingdom


class TriggerAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'prestige_threshold', 'population_threshold')
	search_fields = ('name', 'description')
admin.site.register(Trigger, TriggerAdmin)


class ConstantAdmin (admin.ModelAdmin):
	list_display = ('name', 'description', 'value')
	search_fields = ('name', 'description')
admin.site.register(Constant, ConstantAdmin)


class ValueAdmin(admin.ModelAdmin):
	list_display = ('name', 'kingdom', 'value')
admin.site.register(Value, ValueAdmin)


class FunctionAdmin(admin.ModelAdmin):
	list_display = ('slug', 'description')
admin.site.register(Function, FunctionAdmin)


class RecurringAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'frequency')
	search_fields = ('name', 'description')
	actions = ['resolve']

	def resolve(self, request, queryset):
		kingdoms = Kingdom.objects.all()
		for recurring in queryset:
			for kingdom in kingdoms:
				if recurring.check_condition(kingdom) == "ok":
					recurring.fire(kingdom)
		self.message_user(request, "Les recurrings ont été lancés")
	resolve.short_description = "Do it now"
admin.site.register(Recurring, RecurringAdmin)


class FirstNameAdmin(admin.ModelAdmin):
	list_filter = ('sex',)
	list_display = ('name', 'sex')
	search_fields = ('name',)
admin.site.register(FirstName, FirstNameAdmin)


admin.site.register(LastName)


admin.site.register(Avatar)
