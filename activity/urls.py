from django.conf.urls import patterns, include, url

urlpatterns = patterns('activity.views',
    #url(r'^get_district/$','get_district'),
    url(r'^like/(?P<activityFeed_id>\d+)/$','like'),

)
