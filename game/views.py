from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from models import League, Game, Score, FreeLeagueGame
from forms import ScoreCreationForm, GameEditForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import auth, messages
from datetime import datetime
from notification.models import Notification

@login_required
def join_league(request, league_match_id=1):
	user = request.user.profile
	if user.first_name is None or user.first_name == ''\
		or user.last_name is None or user.last_name == ''\
		or user.phone is None or user.phone == ''\
		or user.level is None or user.level == '':
		return render_to_response('profile_notify.html')
	league_match = League.objects.get(id=league_match_id)
	if League.objects.filter(id=league_match_id,players=user).count()==0:
		league_match.players.add(user)
		league_match.current_player_number += 1
		league_match.save()
	return HttpResponseRedirect('/game/all_league/')

@login_required
def join_league_cancel(request, league_match_attended_id=1):
	user = request.user.profile
	league_match_attended = League.objects.get(id=league_match_attended_id)
	if League.objects.filter(id=league_match_attended_id,players=user).count()!=0:
		league_match_attended.current_player_number -= 1
		league_match_attended.save()
		league_match_attended.players.remove(user)
	return HttpResponseRedirect('/game/all_league/')

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
		score_form = ScoreCreationForm(request.POST,instance=score)
		game_form = GameEditForm(request.POST, instance=game)
		if score_form.is_valid() and game_form.is_valid():
			score_form.save()
			game_form.save()
			confirm_score(request,game_id=game.id)
			if game.player1 == user:
				Notification.objects.create(user = game.player2.user,
											title = 'A game needs to be confirmed',
											message = 'Your game vs %s %s needs your confirmation, go to game page to confirm.' % (game.player1.last_name, game.player1.first_name),
											time = datetime.now())
			else:
				Notification.objects.create(user = game.player1.user,
											title = 'A game needs to be confirmed',
											message = 'Your game vs %s %s needs your confirmation, go to game page to confirm.' % (game.player2.last_name, game.player2.first_name),
											time = datetime.now())

			return HttpResponseRedirect('/game/ladder_game/')
	else:
		score_form = ScoreCreationForm(instance=score)
		game_form = GameEditForm(instance=game)

	args = {}
	args.update(csrf(request))

	args['profile'] = user
	args['score_form'] = score_form
	args['game_form'] = game_form
	args['player1'] = game.player1
	args['player2'] = game.player2
	args['game_id'] = game.id
	return render_to_response('upload-score.html', args)



@login_required
def confirm_score(request,game_id = 1):
	user = request.user.profile
	game = Game.objects.get(id = game_id)
	if game.player1 != user and game.player2 != user:
		auth.logout(request)
		return HttpResponseRedirect('/account/login')
	if game.player1 == user:
		game.player1_confirmed = True
		if game.player2_confirmed:
			game.winner = get_winner(game)
			Notification.objects.create(user = game.player1.user,
										title = 'A game is completed',
										message = 'Your game against %s %s is completed' % (game.player2.last_name, game.player2.first_name),
										time = datetime.now())
			Notification.objects.create(user = game.player2.user,
										title = 'A game is completed',
										message = 'Your game against %s %s is completed' % (game.player1.last_name, game.player1.first_name),
										time = datetime.now())
		game.save()

		return HttpResponseRedirect('/game/ladder_game/')
	else:
		game.player2_confirmed = True
		if game.player1_confirmed:
			game.winner = get_winner(game)
			Notification.objects.create(user = game.player1.user,
										title = 'A game is completed',
										message = 'Your game against %s %s is completed' % (game.player2.last_name, game.player2.first_name),
										time = datetime.now())
			Notification.objects.create(user = game.player2.user,
										title = 'A game is completed',
										message = 'Your game against %s %s is completed' % (game.player1.last_name, game.player1.first_name),
										time = datetime.now())
		game.save()
		return HttpResponseRedirect('/game/ladder_game/')

@login_required
def find_game(request):
	"""

	:param request:
	:return:
	"""
	user = request.user.profile
	if user.first_name is None or user.first_name == ''\
		or user.last_name is None or user.last_name == ''\
		or user.phone is None or user.phone == ''\
		or user.level is None or user.level == '':
		return render_to_response('profile_notify.html')
	free_game = FreeLeagueGame.objects.get_or_create(player = user)[0]
	free_game.request_time = datetime.now()
	free_game.save()
	messages.success(request,'join success')
	username = user.last_name+user.first_name
	league_match_attended = League.objects.filter(players=request.user.profile)

	args = {}
	notifications = Notification.objects.filter(user = request.user, viewed = False)
	args['username'] = username
	args['profile'] = user
	args['league_matches_attended'] = league_match_attended
	args['league_matches_remained'] = League.objects.exclude(players=request.user)
	args['notifications'] = notifications
	return render(request, 'page-profile.html', args)



@login_required
def quit_game(request,game_id = 1):
	"""

	:param request:
	:param game_id:
	:return:
	"""
	user = request.user.profile
	game = Game.objects.get(id = game_id)
	if game.player1 != user and game.player2 != user:
		auth.logout(request)
		return HttpResponseRedirect('/account/login/')
	if game.player1 == user:
		Notification.objects.create(user = game.player2.user,
									title = 'One of your opponent has quit a game',
									message = 'Your opponent %s %s quit the game' % (game.player1.last_name, game.player1.first_name),
									time = datetime.now(),)
	else:
		Notification.objects.create(user = game.player1.user,
									title = 'One of your opponent has quit a game',
									message = 'Your opponent %s %s quit the game' % (game.player2.last_name, game.player2.first_name),
									time = datetime.now(),)

	game.delete()
	return HttpResponseRedirect('/game/list_all_games')

def get_winner(game):
	score = Score.objects.get(game = game)

	if score.set1>score.set2:
		return game.player1
	else:
		return game.player2

@login_required
def ladder_game(request):
	user = request.user.profile
	'''
	games_as_player1 = Game.objects.filter(player1 = user)
	games_as_player2 = Game.objects.filter(player2 = user)
	games_played_as_player1 = []
	games_played_as_player2 = []
	for game in games_as_player1:
		if game.is_played:
			games_played_as_player1.append(game)
			games_as_player1 = games_as_player1.exclude(id=game.id)
	for game in games_as_player2:
		if game.is_played:
			games_played_as_player2.append(game)
			games_as_player2 = games_as_player2.exclude(id=game.id)
	'''
	games = Game.objects.filter((Q(player1 = user) | Q(player2 = user)))
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()

	return render_to_response('ladder-game.html',
		{'games': games,
		 'user': user,
		 'notifications': notifications},)

@login_required
def all_league(request):
	user = request.user.profile
	league_all = League.objects.all().order_by('start_date').reverse()
	#league_attended = League.objects.filter(players=request.user.profile)
	#league_attended_finished = league_attended.filter(is_finished = True)
	#league_attended_not_finished = league_attended.filter(is_finished = False)
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()

	args = {}
	args['all_league'] = league_all
	args['profile'] = user
	args['notifications'] = notifications
	return render_to_response('all-league.html', args)

@login_required
def attended_league(request):
	user = request.user.profile
	league_attended = League.objects.filter(players=request.user.profile)
	league_attended_finished = league_attended.filter(is_finished = True).order_by('start_date').reverse()
	league_attended_not_finished = league_attended.filter(is_finished = False).order_by('start_date').reverse()
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()
	notifications = Notification.objects.filter(user = request.user, viewed = False).order_by('time').reverse()

	args = {}
	args['league_attended_finished'] = league_attended_finished
	args['league_attended_not_finished'] = league_attended_not_finished
	args['profile'] = user
	args['notifications'] = notifications
	return render_to_response('attended-league.html', args)
