# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import TextInput
from django.db import models

from config.admin import force_delete, ModelAdmin
from event.models import Event, EventCategory, EventAction, PendingEvent, PendingEventToken


class EventActionAdminInline(admin.StackedInline):
	model = EventAction
	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size': '100'})},
	}

	extra = 0


class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'text', 'weight', 'category', 'thumb',)
	list_display_links = ('name', 'slug')
	list_per_page = 1000

	def thumb(self, obj):
		if obj.image:
			return '<img src="%s" style="width:150px" />' % obj.image.url
	thumb.short_description = 'Image'
	thumb.allow_tags = True

	search_fields = ('name', 'text', 'slug', 'eventaction__message', 'eventaction__text')
	list_filter = ('category__name',)
	inlines = [
		EventActionAdminInline,
	]
	fieldsets = (
		(None, {
			'fields': (('name', 'slug'), 'image', 'text', ('weight', 'category'))
		}),
		('Étapes', {
			'fields': ('condition', 'on_fire')
		})
	)

admin.site.register(Event, EventAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'frequency', 'timeout')
	search_fields = ('name', 'description')
admin.site.register(EventCategory, EventCategoryAdmin)


class PendingEventAdmin(ModelAdmin):
	readonly_fields = ('text',)
	list_display = ('event', 'kingdom', 'started', 'text')
	search_fields = ('event__name', 'text')
	actions = [force_delete]
	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size': '100'})},
	}
admin.site.register(PendingEvent, PendingEventAdmin)


class PendingEventTokenAdmin(ModelAdmin):
	list_display = ('kingdom', 'created', 'pending_event', 'category')
admin.site.register(PendingEventToken, PendingEventTokenAdmin)
