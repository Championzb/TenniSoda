from django.contrib import admin
from city.models import City, District

# Register your models here.
class DistrictAdmin(admin.ModelAdmin):
	list_display = ['city','name']
	list_filter = ('city',)
	ordering = ['city']
	search_fields = ('name', )

class CityAdmin(admin.ModelAdmin):
	list_display = ['name',]
	ordering = ['name']
	search_fields = ('name', )

admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)