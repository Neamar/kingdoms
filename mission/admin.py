# -*- coding: utf-8 -*-
from django.contrib import admin

from mission.models import *


class MissionAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'title', 'category')
admin.site.register(Mission, MissionAdmin)


class MissionGridAdmin(admin.ModelAdmin):
	list_display = ('mission', 'description', 'length')
admin.site.register(MissionGrid, MissionGridAdmin)


class PendingMissionAdmin(admin.ModelAdmin):
	list_display = ('mission', 'kingdom', 'started')
	actions = ['resolve']

	def resolve(self, request, queryset):
		for pendingmission in queryset:
			pendingmission.resolve()
		self.message_user(request, "Les missions ont été résolues")
	resolve.short_description = "Résoudre les missions sélectionnées"

admin.site.register(PendingMission, PendingMissionAdmin)


class PendingMissionAffectationAdmin(admin.ModelAdmin):
	list_display = ('pending_mission', 'mission_grid', 'folk')
admin.site.register(PendingMissionAffectation, PendingMissionAffectationAdmin)


class AvailableMissionAdmin(admin.ModelAdmin):
	list_display = ('mission', 'kingdom')
admin.site.register(AvailableMission, AvailableMissionAdmin)
