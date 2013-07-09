# -*- coding: utf-8 -*-
from django.contrib import admin
from internal.models import Trigger, Constant, Value, Recurring, FirstName, LastName, Function, Avatar, ScriptLog
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
	list_display = ('name', 'description', 'delay')
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


class AvatarAdmin(admin.ModelAdmin):
	list_display = ('sex', 'hair', 'thumb_child', 'thumb_teenager', 'thumb_adult', 'thumb_old')

	def thumb_child(self, obj):
		return '<img src="%s" />' % obj.child.url
	thumb_child.allow_tags = True

	def thumb_teenager(self, obj):
		return '<img src="%s" />' % obj.teenager.url
	thumb_teenager.allow_tags = True

	def thumb_adult(self, obj):
		return '<img src="%s" />' % obj.adult.url
	thumb_adult.allow_tags = True

	def thumb_old(self, obj):
		return '<img src="%s" />' % obj.old.url
	thumb_old.allow_tags = True
admin.site.register(Avatar, AvatarAdmin)


class ScriptLogAdmin(admin.ModelAdmin):
	list_display = ('slug', 'object_type', 'object_pk', 'object_attr', 'kingdom', 'time', 'queries')
	list_filter = ('object_type', 'object_attr')

	def has_add_permission(self, request, obj=None):
		return False

	def slug(self, obj):
		from event.models import Event, EventAction
		from mission.models import Mission
		from title.models import Title
		from kingdom.models import Quality

		classes = {
			'Event': lambda pk: Event.objects.get(pk=pk).slug,
			'EventAction': lambda pk: EventAction.objects.get(pk=pk).event.slug,
			'Mission': lambda pk: Mission.objects.get(pk=pk).slug,
			'Function': lambda pk: Function.objects.get(pk=pk).slug,
			'Title': lambda pk: Title.objects.get(pk=pk).slug,
			'Quality': lambda pk: Quality.objects.get(pk=pk).slug
		}

		if obj.object_type in classes.keys():
			slug = classes[obj.object_type](obj.object_pk)
			return slug

		return '--'
admin.site.register(ScriptLog, ScriptLogAdmin)
