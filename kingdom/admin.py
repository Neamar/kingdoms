# -*- coding: utf-8 -*-
from django.contrib import admin

from config.admin import force_delete
from kingdom.models import Kingdom, Folk, Quality, QualityCategory, Message, Claim


class KingdomAdmin(admin.ModelAdmin):
	list_display = ('user', 'prestige', 'population', 'money', 'soldiers')
	search_fields = ('user__username', )
	readonly_fields = ('values', )
	actions=[force_delete]

	def values(self, obj):
		values = ['%s=%s' % (o[0], o[1]) for o in obj.get_values().items()]
		return '<br /><pre>%s</pre>' % "\n".join(values)
	values.short_description = 'Variables'
	values.allow_tags = True
admin.site.register(Kingdom, KingdomAdmin)


class EventActionAdminInline(admin.StackedInline):
	model = Quality
	extra = 2


class FolkAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'kingdom', 'sex', 'birth', 'thumb')
	search_fields = ('first_name', 'last_name')
	list_filter = ('sex', 'kingdom')
	fieldsets = (
		(None, {
			'fields': ('kingdom', ('first_name', 'last_name'), ('sex', 'avatar'), 'disabled')
		}),
		('Généalogie', {
			'fields': (('mother', 'father'), ('spouse', 'mentor'))
		}),
		('Vie et mort', {
			'classes': ('collapse',),
			'fields': ('birth', 'death')
		}),
		('Attributs', {
			'fields': (('fight', 'diplomacy'), ('plot', 'scholarship'), 'loyalty')
		}),
		('Traits', {
			'fields': ('quality_set',)
		})
	)

	def thumb(self, obj):
		if obj.avatar and not obj.death:
			return '<img src="%s" style="width:50px" />' % obj.avatar.image(obj.age())
	thumb.short_description = 'Image'
	thumb.allow_tags = True
admin.site.register(Folk, FolkAdmin)


class QualityCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name', 'description')
admin.site.register(QualityCategory, QualityCategoryAdmin)


class QualityAdmin(admin.ModelAdmin):
	list_display = ('name', 'female_name', 'slug', 'category', 'description')
	search_fields = ('name', 'description')
	list_filter = ('category__name',)
	ordering=('name',)
admin.site.register(Quality, QualityAdmin)


class MessageAdmin(admin.ModelAdmin):
	list_display = ('kingdom', 'content', 'level', 'read')
admin.site.register(Message, MessageAdmin)


class ClaimAdmin(admin.ModelAdmin):
	list_display = ('offender', 'offended', 'level', 'created')
admin.site.register(Claim, ClaimAdmin)
