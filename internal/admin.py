# -*- coding: utf-8 -*-
from django.contrib import admin
from internal.models import Trigger, Constant, Value, Recurring


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
admin.site.register(Recurring, RecurringAdmin)
