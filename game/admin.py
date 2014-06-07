from django.contrib import admin
from models import League, Game, Score, GroupStage

def game_arrange(modeladmin,request,queryset):
	for league in queryset:
		#arrange game for a league
		group_num = 4

		group_index = 1
		member_index = 0
		for player in league.players.all():
			GroupStage.objects.create(league=league,group_number=group_index,member_number=member_index/group_num+1,player=player)
			group_index = (group_index % group_num) + 1
			member_index += 1

		
class LeagueAdmin(admin.ModelAdmin): 
	list_display = ['name','city','start_date','end_date']
	ordering = ['start_date']
	actions = [game_arrange]

class GroupStageAdmin(admin.ModelAdmin):
	list_display = ['league','group_number','member_number','player','points']

class GameAdmin(admin.ModelAdmin):
	list_display = ['league','court','player1','player2','winner','date']
	ordering = ['date']

class ScoreAdmin(admin.ModelAdmin):
	list_display = ['game','score11','score12','score21','score22','score31','score32','score41','score42','score51','score52','is_confirmed']
		

admin.site.register(League,LeagueAdmin)
admin.site.register(Game,GameAdmin)
admin.site.register(Score,ScoreAdmin)
admin.site.register(GroupStage,GroupStageAdmin)
