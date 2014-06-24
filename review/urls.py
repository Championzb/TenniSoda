from django.conf.urls import patterns, include, url
urlpatterns = patterns('review.views',
	url(r'^court_review/(?P<game_id>\d+)/$', 'court_review'),
	url(r'^rate_review/(?P<game_id>\d+)/$', 'rate_review'),
    url(r'^all_review/(?P<game_id>\d+)/$', 'all_review'),
)

