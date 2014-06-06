from django.contrib import admin
from models import League, Game, Score, GroupStage

def game_arrange(modeladmin,request,queryset):
	for league in queryset:
		#arrange game for a league
		print league.id

class LeagueAdmin(admin.ModelAdmin): 
	list_display = ['name','city','start_date','end_date']
	ordering = ['start_date']
	actions = [game_arrange]
		

admin.site.register(League,LeagueAdmin)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(GroupStage)
