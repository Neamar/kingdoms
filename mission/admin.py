# -*- coding: utf-8 -*-
from django.contrib import admin

from config.admin import force_delete
from mission.models import Mission, MissionGrid, PendingMission, PendingMissionAffectation, AvailableMission


class MissionGridInline(admin.StackedInline):
	model = MissionGrid
	extra = 0


class MissionAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'text', 'title')
	search_fields = ('name', 'text', 'slug')
	list_filter = ('title__name',)
	inlines = [MissionGridInline]
	fieldsets = (
		(None, {
			'fields': (('name', 'slug'), 'text', ('duration', 'timeout'), 'title', ('is_cancellable', 'is_team'))
		}),
		('Étapes', {
			'fields': ('on_init', 'on_start', 'on_resolution', 'on_cancel')
		}),
		('Cible', {
			'classes': ('collapse',),
			'fields': (('has_target', 'target_description'), 'target_list', )
		}),
		('Valeur', {
			'classes': ('collapse',),
			'fields': (('has_value', 'value_description'),)
		}),
	)

admin.site.register(Mission, MissionAdmin)


class PendingMissionAffectationInline(admin.StackedInline):
	model = PendingMissionAffectation
	extra = 0


class PendingMissionAdmin(admin.ModelAdmin):
	list_display = ('mission', 'kingdom', 'target', 'started')
	actions = ['resolve', force_delete]
	inlines = [PendingMissionAffectationInline]

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		field = super(PendingMissionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		
		if db_field.name == "target":
			
			if request.__temp_pendingmission:
				field.queryset = request.__temp_pendingmission.targets()
		return field

	def get_form(self, request, obj=None, **kwargs):
		request.__temp_pendingmission = obj
		return super(PendingMissionAdmin, self).get_form(request, obj, **kwargs)

	def resolve(self, request, queryset):
		for pendingmission in queryset:
			pendingmission.resolve()
		self.message_user(request, "Les missions ont été résolues")
	resolve.short_description = "Résoudre les missions sélectionnées"

admin.site.register(PendingMission, PendingMissionAdmin)


class AvailableMissionAdmin(admin.ModelAdmin):
	list_display = ('mission', 'kingdom')
	list_filter = ('mission',)
admin.site.register(AvailableMission, AvailableMissionAdmin)
