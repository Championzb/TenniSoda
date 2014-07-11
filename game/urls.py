from django.conf.urls import patterns, include, url
urlpatterns = patterns('game.views',
	url(r'^join_league/(?P<league_match_id>\d+)/$', 'join_league'),
	url(r'^join_league_cancel/(?P<league_match_attended_id>\d+)/$', 'join_league_cancel'),
    url(r'^list_all_games/$', 'list_all_games'),
    url(r'^upload_score/(?P<game_id>\d+)/$', 'upload_score'),
    url(r'^confirm_score/(?P<game_id>\d+)/$', 'confirm_score'),
    url(r'^find_game/$','find_game'),
    url(r'^quit_game/(?P<game_id>\d+)/$','quit_game'),
    url(r'^ladder_game/$', 'ladder_game'),
    url(r'^all_league/$', 'all_league'),
    url(r'^attended_league/$', 'attended_league'),
    url(r'^game_group/$', 'game_group'),
#	url(r'^Find/$', 'LeagueMatch.views.find'),
#	url(r'^CreateMatch/$', 'LeagueMatch.views.create_match'),

)
