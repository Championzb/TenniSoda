from django.contrib import admin
from models import League, Game, Score, GroupStage

def game_arrange(modeladmin,request,queryset):
	for league in queryset:
		#arrange game for a league
		group_num = 1
		member_num = 1
		for player in league.players.all():
			if member_num < 5:
				GroupStage.objects.create(league=league,group_number=group_num,member_number=member_num,player=player)
				member_num += 1
			else:
				group_num += 1
				member_num = 1
				GroupStage.objects.create(league=league,group_number=group_num,member_number=member_num,player=player)
				
		
class LeagueAdmin(admin.ModelAdmin): 
	list_display = ['name','city','start_date','end_date']
	ordering = ['start_date']
	actions = [game_arrange]
		

admin.site.register(League,LeagueAdmin)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(GroupStage)
