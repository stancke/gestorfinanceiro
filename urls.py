from django.conf.urls.defaults import patterns, include, url
import os
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gestorfinanceiro.views.home', name='home'),
    # url(r'^gestorfinanceiro/', include('gestorfinanceiro.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
         (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'media')}),
     (r'^static/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
    (r'^resultados/$', 'gestorfinanceiro.resultados.views.index'),
    (r'^resultados/(?P<url>\w+)/$', 'gestorfinanceiro.resultados.views.resultados'),
    (r'^saidas/$', 'gestorfinanceiro.resultados.views.getAllSaidas'),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
