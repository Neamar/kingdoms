from django.contrib import admin
from event.models import Event, EventCategory, EventAction, PendingEvent, PendingEventAction


class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'weight', 'category',)
admin.site.register(Event, EventAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'frequency', 'timeout')
admin.site.register(EventCategory, EventCategoryAdmin)


class EventActionAdmin(admin.ModelAdmin):
	list_display = ('name', 'event')
admin.site.register(EventAction, EventActionAdmin)


class PendingEventAdmin(admin.ModelAdmin):
	list_display = ('event', 'kingdom', 'creation')
admin.site.register(PendingEvent, PendingEventAdmin)


class PendingEventActionAdmin (admin.ModelAdmin):
	list_display = ('pending_event', 'text', 'folk')
admin.site.register(PendingEventAction, PendingEventActionAdmin)
