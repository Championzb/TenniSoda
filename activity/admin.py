from django.contrib import admin
from models import ActivityFeed

# Register your models here.
class ActivityFeedAdmin(admin.ModelAdmin):
    list_display = ['type', 'date_time', 'creator', 'game_group', 'league', 'game', 'like_num']
    ordering = ['date_time']
    list_filter = ['type']

admin.site.register(ActivityFeed, ActivityFeedAdmin)