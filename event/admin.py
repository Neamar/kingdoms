# -*- coding: utf-8 -*-
from django.contrib import admin
from event.models import Event, EventCategory, EventAction, PendingEvent, PendingEventAction


class EventActionAdminInline(admin.StackedInline):
	model = EventAction
	extra = 0


class EventAdmin(admin.ModelAdmin):
	list_display = ('slug', 'text', 'weight', 'category',)
	list_filter = ('category__name',)
	inlines = [
		EventActionAdminInline,
	]

admin.site.register(Event, EventAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'frequency', 'timeout')
admin.site.register(EventCategory, EventCategoryAdmin)


class PendingEventAdmin(admin.ModelAdmin):
	readonly_fields = ('text',)
	list_display = ('event', 'kingdom', 'started', 'text')
admin.site.register(PendingEvent, PendingEventAdmin)


class PendingEventActionAdmin (admin.ModelAdmin):
	list_display = ('pending_event', 'text', 'folk')
	actions = ['fire']

	def fire(self, request, queryset):
		for pendingevent in queryset:
			pendingevent.fire()
		self.message_user(request, "Les évènements ont été résolus")
	fire.short_description = "Résoudre les évènements sélectionnés"
admin.site.register(PendingEventAction, PendingEventActionAdmin)
