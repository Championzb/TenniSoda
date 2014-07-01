from django.contrib import admin
from city.models import City, District

# Register your models here.
class DistrictAdmin(admin.ModelAdmin):
	list_display = ['city','name']
	ordering = ['city']

admin.site.register(City)
admin.site.register(District, DistrictAdmin)