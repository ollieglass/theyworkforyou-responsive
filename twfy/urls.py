from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('core.views',
    url(r'^$', 'index', name='index'),
    url(r'^mp/(?P<mp_id>\d+)/', 'mp'),
    url(r'^lookup/$', 'lookup'),

    url(r'^mp_api/(?P<mp_id>\d+)/', 'mp_info'),
    # url(r'^api/mp_info/(?P<mp_id>\d+)/', 'mp_info'),
)

urlpatterns += staticfiles_urlpatterns()