from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import League, Game, Score
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def join_league(request, league_match_id=1):
	user = request.user.profile
	league_match = League.objects.get(id=league_match_id)
	if League.objects.filter(id=league_match_id,players=user).count()==0:
		league_match.players.add(user)
		league_match.current_player_number += 1
		league_match.save()
	return HttpResponseRedirect('/account/welcome_user')

@login_required
def join_league_cancel(request, league_match_attended_id=1):
	user = request.user.profile
	league_match_attended = League.objects.get(id=league_match_attended_id)
	if League.objects.filter(id=league_match_attended_id,players=user).count()!=0:
		league_match_attended.current_player_number -= 1
		league_match_attended.save()
		league_match_attended.players.remove(user)
	return HttpResponseRedirect('/account/welcome_user')

@login_required
def list_all_games(request):
	user = request.user.profile
	games_as_player1 = Game.objects.filter(player1 = user)
	games_as_player2 = Game.objects.filter(player2 = user)
	games_played_as_player1 = []
	games_played_as_player2 = []
	for game in games_as_player1:
		if Score.objects.filter(game=game):
			games_played_as_player1.append(game)
			games_as_player1 = games_as_player1.exclude(id=game.id)
			print game.id
	for game in games_as_player2:
		if Score.objects.filter(game=game):
			games_played_as_player2.append(game)
			games_as_player2 = games_as_player2.exclude(id=game.id)
	print games_as_player1
	print games_as_player2
	print games_played_as_player1
	print games_played_as_player2
	return render_to_response('list_all_games.html',
		{'games_as_player1':games_as_player1,
		 'games_as_player2':games_as_player2,
		 'games_played_as_player1':games_played_as_player1,
		 'games_played_as_player2':games_played_as_player2},)