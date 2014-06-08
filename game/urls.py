from django.conf.urls import patterns, include, url
urlpatterns = patterns('game.views',
	url(r'^join_league/(?P<league_match_id>\d+)/$', 'join_league'),
	url(r'^join_league_cancel/(?P<league_match_attended_id>\d+)/$', 'join_league_cancel'),
    url(r'^list_all_games/$', 'list_all_games'),
#	url(r'^Find/$', 'LeagueMatch.views.find'),
#	url(r'^CreateMatch/$', 'LeagueMatch.views.create_match'),

)
