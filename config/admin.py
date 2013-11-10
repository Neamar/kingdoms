# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib import admin
from suit.widgets import LinkedSelect

from config.lib.disable_signals import DisableSignals


def force_delete(modeladmin, request, queryset):
	"""
	Remove an item, without using signals constraints.
	"""
	with DisableSignals():
		queryset.delete()

force_delete.short_description = "Supprimer de force"


class LinkedForm(ModelForm):
	class Meta:
		widgets = {
			'event': LinkedSelect,
			'mission': LinkedSelect,
			'title': LinkedSelect
		}


class ModelAdmin(admin.ModelAdmin):
	form = LinkedForm
