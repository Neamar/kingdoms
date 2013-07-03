# -*- coding: utf-8 -*-
from django.contrib import admin
from event.models import Event, EventCategory, EventAction, PendingEvent, PendingEventAction


class EventActionAdminInline(admin.StackedInline):
	model = EventAction
	extra = 0


class EventAdmin(admin.ModelAdmin):
	list_display = ('slug', 'name', 'text', 'weight', 'category',)
	search_fields = ('name', 'text')
	list_filter = ('category__name')
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
