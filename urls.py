from django.conf.urls.defaults import patterns, include, url
import os
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'media')}),
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
    (r'^resultados/$', 'gestorfinanceiro.resultados.views.index'),
    (r'^resultados/(?P<url>\w+)/$', 'gestorfinanceiro.resultados.views.resultados'),
    (r'^saidas/$', 'gestorfinanceiro.resultados.views.getAllSaidas'),
    #(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dbr/', include('dbr.urls')),
)
