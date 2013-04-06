from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('core.views',
    url(r'^$', 'index', name='index'),
    url(r'^mp/(?P<mp_id>\d+)/', 'mp'),
    url(r'^mp_api/(?P<mp_id>\d+)/', 'mp_api_hack'),
    url(r'^lookup/$', 'lookup'),
)

urlpatterns += staticfiles_urlpatterns()