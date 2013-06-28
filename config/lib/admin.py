from django.contrib import admin


class DescribedModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
