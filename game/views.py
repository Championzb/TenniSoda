from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import League, Game, Score
from forms import ScoreCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import auth

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
		if game.is_played:
			games_played_as_player1.append(game)
			games_as_player1 = games_as_player1.exclude(id=game.id)
			print game.id
	for game in games_as_player2:
		if game.is_played:
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

@login_required
def upload_score(request, game_id=1):
	user = request.user.profile
	game = Game.objects.get(id = game_id)
	if game.player1 != user and game.player2 != user:
		auth.logout(request)
		return HttpResponseRedirect('/account/login')

	score = game.score

	if request.method == 'POST':
		game.is_played = True
		game.player1_confirmed = False
		game.player2_confirmed = False
		game.save()
		form = ScoreCreationForm(request.POST,instance=score)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/game/list_all_games')
	else:
		form = ScoreCreationForm(instance=score)

	args = {}
	args.update(csrf(request))

	args['form'] = form
	args['player1'] = game.player1
	args['player2'] = game.player2
	args['game_id'] = game.id
	return render_to_response('upload_score.html', args)



@login_required
def confirm_score(request,game_id = 1):
	user = request.user.profile
	game = Game.objects.get(id = game_id)
	if game.player1 != user and game.player2 != user:
		auth.logout(request)
		return HttpResponseRedirect('/account/login')
	print 'hellohello'
	if game.player1 == user:
		game.player1_confirmed = True
		if game.player2_confirmed:
			game.winner = get_winner(game)
		game.save()
		return HttpResponseRedirect('/game/list_all_games')
	else:
		game.player2_confirmed = True
		if game.player1_confirmed:
			game.winner = get_winner(game)
		game.save()
		return HttpResponseRedirect('/game/list_all_games')

def get_winner(game):
	score = Score.objects.get(game = game)
	player1_set_point = 0
	player2_set_point = 0
	if score.score11>score.score12:
		player1_set_point += 1
	elif score.score11<score.score12:
		player2_set_point += 1

	if score.score21>score.score22:
		player1_set_point += 1
	elif score.score11<score.score12:
		player2_set_point += 1

	if score.score31>score.score32:
		player1_set_point += 1
	elif score.score11<score.score12:
		player2_set_point += 1

	if score.score41>score.score42:
		player1_set_point += 1
	elif score.score11<score.score12:
		player2_set_point += 1

	if score.score51>score.score52:
		player1_set_point += 1
	elif score.score11<score.score12:
		player2_set_point += 1

	if player1_set_point>player2_set_point:
		return game.player1
	else:
		return game.player2

