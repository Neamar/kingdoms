# -*- coding: utf-8 -*-
from django.contrib import admin

from bargain.models import PendingBargain, PendingBargainKingdom, PendingBargainSharedMission, PendingBargainSharedMissionAffectation


class PendingBargainKingdomAdminInline(admin.StackedInline):
	model = PendingBargainKingdom
	extra = 2
	max_num = 2


class PendingBargainAdmin(admin.ModelAdmin):
	list_display = ('started', 'first_kingdom', 'first_kingdom_state', 'second_kingdom', 'second_kingdom_state')
	inlines = [
		PendingBargainKingdomAdminInline,
	]

	def first_kingdom(self, obj):
		return obj.pendingbargainkingdom_set.all()[0].kingdom

	def first_kingdom_state(self, obj):
		return obj.pendingbargainkingdom_set.all()[0].get_state_display()

	def second_kingdom(self, obj):
		return obj.pendingbargainkingdom_set.all()[1].kingdom

	def second_kingdom_state(self, obj):
		return obj.pendingbargainkingdom_set.all()[1].get_state_display()

admin.site.register(PendingBargain, PendingBargainAdmin)


class PendingBargainSharedMissionAffectationAdminInline(admin.StackedInline):
	model = PendingBargainSharedMissionAffectation
	extra = 1


class PendingBargainSharedMissionAdmin(admin.ModelAdmin):
	model = PendingBargainSharedMission

	inlines = [
		PendingBargainSharedMissionAffectationAdminInline,
	]
admin.site.register(PendingBargainSharedMission, PendingBargainSharedMissionAdmin)
