# -*- coding: utf-8 -*-
from django.contrib import admin

from mission.models import Mission, MissionGrid, PendingMission, PendingMissionAffectation, AvailableMission


class MissionGridInline(admin.StackedInline):
	model = MissionGrid
	extra = 0


class MissionAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'text', 'title')
	list_filter = ('title__name',)
	inlines = [MissionGridInline]

admin.site.register(Mission, MissionAdmin)


class PendingMissionAffectationInline(admin.StackedInline):
	model = PendingMissionAffectation
	extra = 0


class PendingMissionAdmin(admin.ModelAdmin):
	list_display = ('mission', 'kingdom', 'target', 'started')
	actions = ['resolve']
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
admin.site.register(AvailableMission, AvailableMissionAdmin)
