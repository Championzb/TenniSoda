from django.contrib import admin
from models import League, Game, Score, GroupStage

def game_arrange(modeladmin,request,queryset):
	for league in queryset:
		#arrange game for a league
		for player in league.players.all():
			GroupStage.objects.create(league=league,group_number=1,member_number=1,player=player)
		
class LeagueAdmin(admin.ModelAdmin): 
	list_display = ['name','city','start_date','end_date']
	ordering = ['start_date']
	actions = [game_arrange]
		

admin.site.register(League,LeagueAdmin)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(GroupStage)
