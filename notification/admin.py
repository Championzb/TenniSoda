from django.contrib import admin
from models import Notification
# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title','message', 'viewed', 'time']
    ordering = ['user', 'time']
    search_fields = ('title', 'message', )

admin.site.register(Notification, NotificationAdmin)
