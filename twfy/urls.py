from django.conf.urls import patterns, include, url


urlpatterns = patterns('core.views',
    url(r'^$', 'index', name='index'),
    url(r'^mp/(?P<mp_id>\d+)/', 'mp'),
    url(r'^mp_api/(?P<mp_id>\d+)/', 'mp_api'),
    url(r'^lookup/$', 'lookup'),
)

