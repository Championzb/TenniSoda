from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import League
from django.core.context_processors import csrf


def join_league(request, league_match_id=1):
	user = request.user.profile
	league_match = League.objects.get(id=league_match_id)
	league_match.players.add(user)
	league_match.current_player_number += 1
	league_match.save()
	return HttpResponseRedirect('/account/welcome_user')


def join_league_cancel(request, league_match_attended_id=1):
	user = request.user.profile
	league_match_attended = League.objects.get(id=league_match_attended_id)
	league_match_attended.current_player_number -= 1
	league_match_attended.save()
	league_match_attended.players.remove(user)
	return HttpResponseRedirect('/account/welcome_user')
