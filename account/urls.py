from django.conf.urls import patterns, include, url

urlpatterns = patterns('account.views',
    url(r'^register/$','register_user'),
    url(r'^register_success/$', 'register_success'),
    url(r'^login/$','login'),
    url(r'^auth/$', 'auth_view'),
    url(r'^logout/$','logout'),
    url(r'^welcome_user/$', 'welcome_user'),
    url(r'^invalid_login/$', 'invalid_login'),
    url(r'^profile/$', 'change_profile'),

)
