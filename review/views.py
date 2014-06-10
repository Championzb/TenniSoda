from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import CourtReview, RateReview
from forms import CourtReviewCreationForm, RateReviewCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from game.models import Game
from django.contrib import auth
from datetime import datetime

@login_required
def rate_review(request,game_id=1):
	user = request.user.profile
	game = Game.objects.get(id = game_id)
	if game.player1 != user and game.player2 != user:
		auth.logout(request)
		return HttpResponseRedirect('/account/login')

	if game.player1 == user:
		player = game.player2
	else:
		player = game.player1

	time = datetime.now()
	rate_review_instance = RateReview.objects.get_or_create(game=game,player=player)[0]

	if request.method == 'POST':
		rate_review_instance.reviewed_time = time
		rate_review_instance.save()
		form = RateReviewCreationForm(request.POST,instance = rate_review_instance)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/game/list_all_games')
	else:
		form = RateReviewCreationForm(instance = rate_review_instance)

	args = {}
	args.update(csrf(request))

	args['form'] = form
	args['game_id'] = game.id
	args['player'] = player
	return render_to_response('rate_review.html', args)

@login_required
def court_review(request,game_id=1):
	user = request.user.profile
	game = Game.objects.get(id = game_id)
	court = game.court
	if game.player1 != user and game.player2 != user:
		auth.logout(request)
		return HttpResponseRedirect('/account/login')

	time = datetime.now()
	court_review_instance = CourtReview.objects.get_or_create(game=game,player=user,court=court)[0]

	if request.method == 'POST':
		court_review_instance.reviewed_time = time
		court_review_instance.save()
		form = CourtReviewCreationForm(request.POST,instance=court_review_instance)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/game/list_all_games')
	else:
		form = CourtReviewCreationForm(instance=court_review_instance)

	args = {}
	args.update(csrf(request))

	args['form'] = form
	args['game_id'] = game.id
	args['court'] = court
	return render_to_response('court_review.html', args)