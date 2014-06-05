from django.conf.urls import patterns, include, url
urlpatterns = patterns('game.views',
	url(r'^join/(?P<LeagueMatch_id>\d+)/$', 'join'),
	url(r'^quit/(?P<MyLeagueMatch_id>\d+)/$', 'quit'),
#	url(r'^Find/$', 'LeagueMatch.views.find'),
#	url(r'^CreateMatch/$', 'LeagueMatch.views.create_match'),

)
