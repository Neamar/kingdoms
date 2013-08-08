from django.contrib import admin
from reporting.models import ScriptLog

class ScriptLogAdmin(admin.ModelAdmin):
	list_display = ('slug', 'object_type', 'object_pk', 'object_attr', 'kingdom', 'time', 'queries', 'direct_queries')
	list_filter = ('object_type', 'object_attr')

	def has_add_permission(self, request, obj=None):
		return False

	def slug(self, obj):
		from event.models import Event, EventAction
		from mission.models import Mission, MissionGrid
		from title.models import Title
		from kingdom.models import Quality
		from internal.models import Trigger, Function, Recurring

		classes = {
			'Event': lambda pk: Event.objects.get(pk=pk).slug,
			'EventAction': lambda pk: EventAction.objects.get(pk=pk).event.slug,
			'Mission': lambda pk: Mission.objects.get(pk=pk).slug,
			'MissionGrid': lambda pk: MissionGrid.objects.get(pk=pk).mission.slug + MissionGrid.objects.get(pk=pk).name,
			'Function': lambda pk: Function.objects.get(pk=pk).slug,
			'Title': lambda pk: Title.objects.get(pk=pk).slug,
			'Quality': lambda pk: Quality.objects.get(pk=pk).slug,
			'Trigger': lambda pk: Trigger.objects.get(pk=pk).slug,
			'Recurring': lambda pk: Recurring.objects.get(pk=pk).name,
		}

		if obj.object_type in classes.keys():
			indentation = '&nbsp;&nbsp;&nbsp;' * (obj.stack_level - 1)
			slug = classes[obj.object_type](obj.object_pk)
			return indentation + slug
		return '--'
	slug.allow_tags = True
admin.site.register(ScriptLog, ScriptLogAdmin)
