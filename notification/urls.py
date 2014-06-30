from django.conf.urls import patterns, include, url
urlpatterns = patterns('notification.views',
    url(r'^show/(?P<notification_id>\d+)/$', 'show'),
    url(r'^all/$', 'all'),
    url(r'^mark_as_viewed/(?P<notification_id>\d+)/$', 'mark_as_viewed'),
    url(r'^delete/(?P<notification_id>\d+)/$', 'delete'),
    url(r'^mark_all/$', 'mark_all'),
)

