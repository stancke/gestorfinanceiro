# -*- coding: utf-8 -*-
# Create your views here.

'''
Django Business Reports views
'''

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from dbr.core import document, ireport_factory, get_model_for_path
from dbr.fields import model_fields_tree, model_fields_tree_flat
from dbr.models import Report

MIMES = {
    'html' : 'text/html; charset=utf-8',
    'xml' : 'application/xml; charset=utf-8',
    'pdf' : 'application/pdf',
    'txt' : 'text/plain; charset=utf-8',
    'rst' : 'text/plain; charset=utf-8',
    'odt' : 'application/vnd.oasis.opendocument.text',
    'csv' : 'text/csv; charset=utf-8',
}

def json_response(func):
    def wrap(*args, **kwargs):
        return HttpResponse(
            simplejson.dumps(
                func(*args, **kwargs)
                ),
            mimetype="application/json"
            )
    return wrap


@login_required
def view(request, slug, template_name='dbr/view.html'):
    '''
    Renders the main report's view
    '''
    report_id = Report.objects.get(slug=slug).id
    ireport, messages_list = ireport_factory(slug)
    for m in messages_list:
        messages.add_message(request, *m)
    context = {
        'report' : ireport,
        'report_id' : report_id,
        'report_slug' : slug,
    }
    return render_to_response(
        template_name,
        context,
        context_instance = RequestContext(request)
    )


@login_required
def export(request, slug, fmt):
    '''
    Exports a **report** to any of the supported formats.
    Currently supported formats are:
    - html
    - xml (Docutils dialect)
    - pdf
    - txt
    - rst
    - odt
    - csv
    '''
    ireport = ireport_factory(slug)

    mime = fmt in MIMES and MIMES[fmt] or None

    response = HttpResponse(document(ireport, fmt), mimetype=mime)
    response['Cache-Control'] = 'no-cache'
    if fmt in ('pdf', 'odt', 'csv'):
        response['Content-Disposition'] = 'attachment; filename=report.%s' % fmt

    return response

@login_required
@json_response
def model_fields_json(request):
    model_name = request.GET.get('m', None)
    if model_name:
        model = get_model_for_path(model_name)
        fields_tree = model_fields_tree(model)
        return [
            {
                'value' : field,
                'text' : field,
            }
            for field in
            model_fields_tree_flat(fields_tree, model_name)
        ]
    else:
        return {}

@login_required
@json_response
def field_summary_options_json(request):
    field_name = request.GET.get('f', None)
    if field_name:
        # FIXME: implement
        return []
    else:
        return []