from django.conf.urls import patterns, include, url

urlpatterns = patterns('account.views',
    url(r'^register/$','register_user'),
    url(r'^register_success/$', 'register_success')
)
