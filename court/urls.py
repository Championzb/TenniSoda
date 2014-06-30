from django.conf.urls import patterns, include, url

urlpatterns = patterns('court.views',
    url(r'^all/$','all'),
)
