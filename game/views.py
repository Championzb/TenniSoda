from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import League
from django.core.context_processors import csrf


def join(request, LeagueMatch_id=1):
	user = request.user.profile
	League_Match = League.objects.get(id=LeagueMatch_id)
	League_Match.players.add(user)
	return HttpResponseRedirect('/account/welcome_user')


def quit(request, MyLeagueMatch_id=1):
	user = request.user.profile
	My_League_Match = League.objects.get(id=MyLeagueMatch_id)
	My_League_Match.players.remove(user)
	return HttpResponseRedirect('/account/welcome_user')
