# -*- coding: utf-8 -*-
from config.lib.disable_signals import DisableSignals


def force_delete(modeladmin, request, queryset):
	"""
	Remove an item, without using signals constraints.
	"""
	with DisableSignals():
		queryset.delete()

force_delete.short_description = "Supprimer de force"
