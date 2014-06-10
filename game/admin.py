from django.contrib import admin
from models import League, Game, Score, GroupStage,FreeLeagueGame
import datetime

def game_arrange(modeladmin,request,queryset):
	for league in queryset:
		#arrange game for a league
		number = league.current_player_number
		if number < 10:
			group_num = 1
		elif number < 19:
			group_num = 2
		elif number < 25:
			group_num = 3
		elif number < 37:
			group_num = 4
		else:
			group_num = number / 8
			member_remained = number % 8
			if member_remained > group_num:
				group_num += 1

		#arrange the player into group
		group_index = 1
		member_index = 0
		for player in league.players.all():
			GroupStage.objects.create(league=league,group_number=group_index,member_number=member_index/group_num+1,player=player)
			group_index = (group_index % group_num) + 1
			member_index += 1

		#arrange the game by group
		for i in range(1, group_num+1):
			group_stage_set = GroupStage.objects.filter(league=league, group_number=i)
			group_game_arrange(group_stage_set,league.start_date)



def group_game_arrange(group_stage_set, start_date):
	m = group_stage_set.count() / 2
	aList = [i+1 for i in range(m)]
	bList = [i+m+1 for i in range(m)]
	if group_stage_set.count()% 2 == 0:
		#arrange several rounds
		for i in range(2*m -1):
			#arrange one round by pair
			for j in range(m):
				group_stage1 = group_stage_set.get(member_number=aList[j])
				group_stage2 = group_stage_set.get(member_number=bList[j])
				Game.objects.create(league=group_stage1.league, player1=group_stage1.player, player2=group_stage2.player,date=start_date)
			#rotate the player position & add time
			if m>1:
				start_date += datetime.timedelta(days=7)
				temp = bList[0]
				for j in range(1,m):
					bList[j-1]=bList[j]
				bList[m-1] = aList[m-1]
				for j in range(m-1,1):
					aList[j]=aList[j-1]
				aList[1]=temp
	else:
		vacant_player = group_stage_set.count()
		if vacant_player != 1:
			#arrange several rounds
			for i in range(2*m+1):
				#arrange one round by pair
				for j in range(m):
					group_stage1 = group_stage_set.get(member_number=aList[j])
					group_stage2 = group_stage_set.get(member_number=bList[j])
					Game.objects.create(league=group_stage1.league, player1=group_stage1.player, player2=group_stage2.player,date=start_date)
				#rotate the player position & add time
				start_date += datetime.timedelta(days=7)
				#replace the vacant_player
				temp = bList[0]
				bList[0] = vacant_player
				vacant_player = temp

				temp = bList[0]
				for j in range(1, m):
					bList[j-1]=bList[j]
				bList[m-1]=aList[m-1]
				for j in range(m-1,0):
					aList[j]=aList[j-1]
				aList[0]=temp



		
class LeagueAdmin(admin.ModelAdmin): 
	list_display = ['name','city','start_date','end_date']
	ordering = ['start_date']
	actions = [game_arrange]

class GroupStageAdmin(admin.ModelAdmin):
	list_display = ['league','group_number','member_number','player','points']
	ordering = ['league','group_number','member_number']
	action = [group_game_arrange]

class GameAdmin(admin.ModelAdmin):
	list_display = ['league','court','player1','player2','winner','date','is_played','player1_confirmed','player2_confirmed',]
	ordering = ['date']

class ScoreAdmin(admin.ModelAdmin):
	list_display = ['game','score11','score12','score21','score22','score31','score32','score41','score42','score51','score52',]

class FreeLeagueGameAdmin(admin.ModelAdmin):
    list_display = ['player','request_time']

admin.site.register(League,LeagueAdmin)
admin.site.register(Game,GameAdmin)
admin.site.register(Score,ScoreAdmin)
admin.site.register(GroupStage,GroupStageAdmin)
admin.site.register(FreeLeagueGame, FreeLeagueGameAdmin)
