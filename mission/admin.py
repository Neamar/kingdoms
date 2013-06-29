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
admin.site.register(PendingMission)


admin.site.register(PendingMissionAffectation)


class AvailableMissionAdmin(admin.ModelAdmin):
	list_display = ('mission', 'kingdom')
admin.site.register(AvailableMission, AvailableMissionAdmin)
