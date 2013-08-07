# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import TextInput
from django.db import models

from event.models import Event, EventCategory, EventAction, PendingEvent, PendingEventAction


class EventActionAdminInline(admin.StackedInline):
	model = EventAction
	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size': '100'})},
	}

	extra = 0


class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'text', 'weight', 'category', 'thumb',)
	list_display_links = ('name', 'slug')

	def thumb(self, obj):
		if obj.image:
			return '<img src="%s" style="width:150px" />' % obj.image.url
	thumb.short_description = 'Image'
	thumb.allow_tags = True

	search_fields = ('name', 'text', 'slug')
	list_filter = ('category__name',)
	inlines = [
		EventActionAdminInline,
	]

admin.site.register(Event, EventAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'frequency', 'timeout')
	search_fields = ('name', 'description')
admin.site.register(EventCategory, EventCategoryAdmin)


class PendingEventAdmin(admin.ModelAdmin):
	readonly_fields = ('text',)
	list_display = ('event', 'kingdom', 'started', 'text')
	search_fields = ('event__name', 'text')
admin.site.register(PendingEvent, PendingEventAdmin)


class PendingEventActionAdmin (admin.ModelAdmin):
	list_display = ('pending_event', 'text', 'folk')
	search_fields = ('event__name', 'text')
	actions = ['fire']

	def fire(self, request, queryset):
		for pendingevent in queryset:
			pendingevent.fire()
		self.message_user(request, "Les évènements ont été résolus")
	fire.short_description = "Résoudre les évènements sélectionnés"
admin.site.register(PendingEventAction, PendingEventActionAdmin)
