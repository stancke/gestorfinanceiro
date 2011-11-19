from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'dbr.charts',
    url(r'^chart/(?P<chart_id>.*)/$', 'chart_view', name='dbr-view-chart')
)

urlpatterns += patterns(
    'dbr.views',
    url(
        r'^field_summary_opts/json/$',
        'field_summary_options_json',
        name='dbr-field-summary-opts-json'
    ),
    url(
        r'^model_fields/json/$',
        'model_fields_json',
        name='dbr-model-fields-json'
    ),
    url(
        r'^export/(?P<fmt>.*)/(?P<slug>.*)/$',
        'export',
        name='dbr-export'
    ),
    url(
        r'^(?P<slug>.*)/$',
        'view',
        name='dbr-view'
    ),
)
