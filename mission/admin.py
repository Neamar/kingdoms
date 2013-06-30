# -*- coding: utf-8 -*-
from django.contrib import admin

from mission.models import Mission, MissionGrid, PendingMission, PendingMissionAffectation, AvailableMission


class MissionGridInline(admin.StackedInline):
	model = MissionGrid
	extra = 0


class MissionAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'title', 'category')
	inlines = [MissionGridInline]
admin.site.register(Mission, MissionAdmin)


class PendingMissionAffectationInline(admin.StackedInline):
	model = PendingMissionAffectation
	extra = 1


class PendingMissionAdmin(admin.ModelAdmin):
	list_display = ('mission', 'kingdom', 'target', 'started')
	actions = ['resolve']
	inlines = [PendingMissionAffectationInline]

	def resolve(self, request, queryset):
		for pendingmission in queryset:
			pendingmission.resolve()
		self.message_user(request, "Les missions ont été résolues")
	resolve.short_description = "Résoudre les missions sélectionnées"

admin.site.register(PendingMission, PendingMissionAdmin)


class AvailableMissionAdmin(admin.ModelAdmin):
	list_display = ('mission', 'kingdom')
admin.site.register(AvailableMission, AvailableMissionAdmin)
