from django.contrib import admin
from court.models import Court

class CourtAdmin(admin.ModelAdmin):
	list_display = ['name', 'city', 'address', 'fee','picture', 'position', 'phone',]
	list_filter = ('city',)
	ordering = ['city', 'fee', ]
	search_fields = ('name', 'address', 'phone')

admin.site.register(Court, CourtAdmin)
