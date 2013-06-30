from django.contrib import admin
from event.models import Event, EventCategory, EventAction, PendingEvent, PendingEventAction


class EventActionAdminInline(admin.StackedInline):
	model = EventAction
	extra = 2


class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'weight', 'category',)
	list_filter = ('category__name',)
	inlines = [
		EventActionAdminInline,
	]

admin.site.register(Event, EventAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'frequency', 'timeout')
admin.site.register(EventCategory, EventCategoryAdmin)


class PendingEventAdmin(admin.ModelAdmin):
	list_display = ('event', 'kingdom', 'creation')
admin.site.register(PendingEvent, PendingEventAdmin)


class PendingEventActionAdmin (admin.ModelAdmin):
	list_display = ('pending_event', 'text', 'folk')
admin.site.register(PendingEventAction, PendingEventActionAdmin)
