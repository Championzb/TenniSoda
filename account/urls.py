from django.conf.urls import patterns, include, url

urlpatterns = patterns('account.views',
    url(r'^register/$','register_user'),
    url(r'^login/$','login'),
    url(r'^auth/$', 'auth_view'),
    url(r'^logout/$','logout'),
    url(r'^welcome_user/$', 'welcome_user'),
    url(r'^invalid_login/$', 'invalid_login'),
    url(r'^change_profile/$', 'change_profile'),
    url(r'^view_profile/(?P<user_id>\d+)/$','view_profile'),
    url(r'^change_password/$', 'change_password'),
    url(r'^confirm/(?P<activation_key>\w+)/$', 'confirm'),
    url(r'^confirmation_resend/$', 'confirmation_resend'),
    url(r'^forget_password/$', 'forget_password'),

)
