from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse

from reporting.models import ScriptLog


class ScriptLogAdmin(admin.ModelAdmin):
	list_display = ('slug', 'object_type', 'object_pk', 'object_attr', 'kingdom', 'time', 'queries', 'direct_queries')
	list_filter = ('object_type', 'object_attr')

	def suit_row_attributes(self, obj, request):
		if obj.time > 500:
			return {'class': 'warning'}
		elif obj.time > 1000:
			return {'class': 'error'}

		return

	def has_add_permission(self, request, obj=None):
		return False

	def slug(self, obj):
		from event.models import Event, EventAction
		from mission.models import Mission, MissionGrid
		from title.models import Title
		from kingdom.models import Quality
		from internal.models import Trigger, Function, Recurring

		# Extract meaningful name from object
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


class LogEntryAdmin(admin.ModelAdmin):
	date_hierarchy = 'action_time'
	readonly_fields = LogEntry._meta.get_all_field_names()
	list_filter = [
		'user',
		'content_type',
	]
	search_fields = [
		'object_repr',
		'change_message'
	]
	list_display = [
		'action_time',
		'user',
		'content_type',
		'object_link',
		'action',
		'change_message',
	]

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return request.user.is_superuser and request.method != 'POST'

	def has_delete_permission(self, request, obj=None):
		return False

	def action(self, obj):
		images = [
			'/static/admin/img/icon_changelink.gif',
			'/static/admin/img/icon_addlink.gif',
			'/static/admin/img/icon_deletelink.gif'
		]

		return '<img src="%s" alt="" />' % images[obj.action_flag - 1]
	action.allow_tags = True

	def object_link(self, obj):
		if obj.action_flag == DELETION:
			link = escape(obj.object_repr)
		else:
			ct = obj.content_type
			print ct.app_label, ct.model
			link = u'<a href="%s">%s</a>' % (
				reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
				escape(obj.object_repr),
			)
		return link
	object_link.allow_tags = True
	object_link.admin_order_field = 'object_repr'
	object_link.short_description = u'object'
admin.site.register(LogEntry, LogEntryAdmin)
