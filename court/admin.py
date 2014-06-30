from django.contrib import admin
from court.models import Court

class CourtAdmin(admin.ModelAdmin):
	list_display = ['name', 'city', 'address', 'fee', 'position']
	ordering = ['city']

admin.site.register(Court, CourtAdmin)
