'''
Core document creation routines and helpers
'''

# FIXME: refactor

import csv

from cStringIO import StringIO
from collections import Iterable
from datetime import date

from docutils.core import publish_from_doctree
from docutils.nodes import (bullet_list, colspec, decoration, entry, footer,
                            header, image, list_item, paragraph, row, section,
                            strong, table, tbody, tgroup, thead, title)
from docutils.utils import new_document

try:
    from rst2pdf.createpdf import RstToPdf
    RST2PDF = True
except ImportError:
    RST2PDF = False

from rst2rst import gen_rst

from django.contrib.sites.models import Site
from django.contrib import messages
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import importlib

from dbr.models import (Report, Column, Annotate, Aggregate, Filter, GroupBy,
                        Chart, CustomColumn)

# Formats handled by a docutils writer
DOCUTILS_WRITER_NAMES = (
    'xml',
    'latex',
    's5',
    'html',
    'odt',
    'txt',
    'rst'
)

# Supported formats contains all formats
SUPPORTED_FORMATS = ('pdf', 'csv') + DOCUTILS_WRITER_NAMES

# Map of aggregation/annotation function names
FUNCTION_NAMES_MAP = {
    'Sum': unicode(_('Sum')),
    'Avg': unicode(_('Average')),
    'Count': unicode(_('Count')),
    'Max': unicode(_('Maximum')),
    'Min': unicode(_('Minimum')),
    'StdDev': unicode(_('Standard Deviation')),
    'Variance': unicode(_('Variance')),
}

# Aggregations for custom columns
# TODO: Check if it's possible to use Django aggregations here
# It's not very effective.

import math

cc_avg = lambda x: sum(x) / len(x)
cc_variance = lambda x: sum([(i - cc_avg(x)) ** 2 for i in x]) / len(x)
cc_stddev = lambda x: math.sqrt(cc_variance(x))

CC_AGGREGATION_FUNCS = {
    'Sum': sum,
    'Avg': cc_avg,
    'Count': len,
    'Max': max,
    'Min': min,
    'StdDev': cc_stddev,
    'Variance': cc_variance,
}


def doctree_factory(report, fmt='html'):
    '''
    Takes a report and builds an adequated doctree for it
    '''
    report = report[0]
    # Create the doctree and set the document title
    doctree = new_document('<string>')
    doctree.setdefault('title', report.title)
    # Report's main title
    doctree.append(title(text=report.title))
    # Setup header and footer
    doc_decoration = decoration()
    doc_header = header()
    doc_header.append(paragraph(text=report.title))
    doc_decoration.append(doc_header)
    doc_footer = footer()
    date_str = date.today().strftime("%d/%m/%Y")
    doc_footer.append(paragraph(text=date_str))
    doc_decoration.append(doc_footer)
    doctree.append(doc_decoration)
    # Report's description
    s_description = section()
    doc_desc_title = paragraph()
    doc_desc_title.append(strong(text=_('Description')))
    s_description.append(doc_desc_title)
    s_description.append(paragraph(text=report.description))
    doctree.append(s_description)
    # List of active filters
    if report.filters:
        s_filters = section()
        doc_filters_title = paragraph()
        doc_filters_title.append(strong(text=_('Active Filters')))
        s_filters.append(doc_filters_title)
        filters_list = bullet_list(bullet='*')
        for filt in report.filters:
            l_item = list_item()
            filt_text = '%s %s %s' % ((filt[0],) + filt[2:4])
            l_item.append(paragraph(text=filt_text))
            filters_list.append(l_item)
        s_filters.append(filters_list)
        doctree.append(s_filters)
    # Data table(s)
    # If there are no groupings, show one table with all (filtered) data
    if not report.groupings:
        s_table = section()
        t_table = table()
        t_group = tgroup()
        t_group.setdefault('cols', len(report.columns))
        for col in report.columns:
            cspec = colspec()
            cspec.setdefault('colwidth', int(col['width']))
            t_group.append(cspec)
        t_head = thead()
        t_head_row = row()
        for col in report.columns:
            c_entry = entry()
            c_entry.append(paragraph(text=col['title']))
            t_head_row.append(c_entry)
        t_head.append(t_head_row)
        t_group.append(t_head)
        t_body = tbody()
        for r_row in report.rows:
            t_row = row()
            for r_cell in r_row:
                t_entry = entry()
                if r_cell['type'] == 'object':
                    t_entry.append(paragraph(text=r_cell['obj']))
                elif r_cell['type'] == 'iterable':
                    objects_list = bullet_list(bullet='*')
                    for element in r_cell['obj']:
                        ol_item = list_item()
                        c_item = paragraph(text=element)
                        ol_item.append(paragraph(text=element))
                        objects_list.append(ol_item)
                    t_entry.append(objects_list)
                t_row.append(t_entry)
            t_body.append(t_row)
        # Aggregations
        if report.has_aggregations:
            t_row = row()
            for aggr in report.aggregations:
                t_entry = entry()
                if aggr:
                    t_entry.append(paragraph(text='%.2f (%s)' % (aggr)))
                t_row.append(t_entry)
            t_body.append(t_row)
        t_group.append(t_body)
        t_table.append(t_group)
        s_table.append(t_table)
        doctree.append(s_table)
    else:
        # If there are groups, setup a table for every group.
        # Also, add a list of groupings.
        s_groups_list = section()
        doc_groups_title = paragraph()
        doc_groups_title.append(strong(text=_('Active Groupings')))
        s_groups_list.append(doc_groups_title)
        groups_list = bullet_list(bullet='*')
        for r_group in report.groupings:
            l_item = list_item()
            l_item.append(paragraph(text=r_group.capitalize()))
            groups_list.append(l_item)
        s_groups_list.append(groups_list)
        doctree.append(s_groups_list)
        for r_group in report.groupings:
            # Dummy paragraph for spacing
            s_table = section()
            s_table.append(paragraph())
            if len(report.groupings) > 1:
                s_table.append(
                    paragraph(
                        text=_('Grouped By') + ' %s' % r_group.capitalize()
                    )
                )
            for ind, choice in getattr(
                report, 'grouping_choices_%s' % r_group
            ):
                # Table group title
                p_table_title = paragraph()
                p_table_title.append(strong(text=choice))
                s_table.append(p_table_title)
                t_table = table()
                t_group = tgroup()
                t_group.setdefault('cols', len(report.columns))
                for col in report.columns:
                    cspec = colspec()
                    cspec.setdefault('colwidth', int(col['width']))
                    t_group.append(cspec)
                t_head = thead()
                t_head_row = row()
                for col in report.columns:
                    c_entry = entry()
                    c_entry.append(paragraph(text=col['title']))
                    t_head_row.append(c_entry)
                t_head.append(t_head_row)
                t_group.append(t_head)
                t_body = tbody()
                group_rows = getattr(report, 'rows_%s' % choice)
                for g_row in group_rows:
                    t_row = row()
                    for r_cell in r_row:
                        t_entry = entry()
                        if r_cell['type'] == 'object':
                            t_entry.append(paragraph(text=r_cell['obj']))
                        elif r_cell['type'] == 'iterable':
                            objects_list = bullet_list(bullet='*')
                            for element in r_cell['obj']:
                                ol_item = list_item()
                                c_item = paragraph(text=element)
                                ol_item.append(c_item)
                                objects_list.append(ol_item)
                            t_entry.append(objects_list)
                    t_row.append(t_entry)
                    t_body.append(t_row)
                    t_row = row()
                    for r_cell in g_row:
                        t_entry = entry()
                        t_entry.append(paragraph(text=r_cell))
                        t_row.append(t_entry)
                    t_body.append(t_row)
                # Aggregations
                if report.aggregations:
                    t_row = row()
                    for aggr in getattr(report, 'aggregations_%s' % choice):
                        t_entry = entry()
                        if aggr and aggr[0]:
                            t_entry.append(
                                paragraph(text='%.2f (%s)' % (aggr))
                            )
                        t_row.append(t_entry)
                    t_body.append(t_row)
                t_group.append(t_body)
                t_table.append(t_group)
                s_table.append(t_table)
            doctree.append(s_table)
            if report.aggregations:
                summary = section()
                summary.append(paragraph())
                p_summary_title = paragraph()
                p_summary_title.append(strong(text=_('Summary')))
                summary.append(p_summary_title)
                st_table = table()
                st_group = tgroup()
                st_group.setdefault('cols', len(report.columns))
                for col in report.columns:
                    cspec = colspec()
                    cspec.setdefault('colwidth', int(col['width']))
                    st_group.append(cspec)
                st_head = thead()
                st_head_row = row()
                for c in report.columns:
                    c_entry = entry()
                    c_entry.append(paragraph(text=c['title']))
                    st_head_row.append(c_entry)
                st_head.append(st_head_row)
                st_group.append(st_head)
                st_body = tbody()
                st_row = row()
                for aggr in report.aggregations:
                    st_entry = entry()
                    if aggr:
                        st_entry.append(paragraph(text='%.2f (%s)' % (aggr)))
                    st_row.append(st_entry)
                st_body.append(st_row)
            st_group.append(st_body)
            st_table.append(st_group)
            summary.append(st_table)
            doctree.append(summary)
    # Charts Handling
    # odt writer support for external images is not working
    if report.charts and fmt != 'odt':
        s_charts = section()
        p_charts_title = paragraph()
        charts_title = strong(text=_('Charts'))
        p_charts_title.append(charts_title)
        s_charts.append(p_charts_title)
        for chart in report.charts:
            s_chart = section()
            p_chart_title = paragraph(text=chart['field'].capitalize())
            s_chart.append(p_chart_title)
            i_chart = image(
                uri=chart['uri'],
                width='70%',
            )
            s_chart.append(i_chart)
            s_charts.append(s_chart)
        doctree.append(s_charts)
    return doctree


def report2csv(report):
    '''
    Generates a CSV file from a report's data
    '''
    report = report[0]
    buff = StringIO()
    csv_out = csv.writer(buff)
    csv_out.writerow([x['title'] for x in report.columns])
    for r_row in report.rows:
        n_row = [
            (
                el['obj'].encode('utf-8') if isinstance(
                    el['obj'],
                    (basestring, unicode)
                ) else unicode(el['obj'])
            )
            for el in r_row
        ]
        csv_out.writerow(n_row)
    return buff.getvalue()


def document(report, fmt='html'):
    '''
    Creates a document in the desired `fmt`. Defaults to html.
    '''

    if fmt == 'csv':
        return report2csv(report)

    doctree = doctree_factory(report, fmt=fmt)

    dt_settings = {
        'input_encoding': 'unicode',
    }

    if fmt == 'pdf':
        if not RST2PDF:
            raise Exception('rst2pdf is not available')
            return None
        buff = StringIO()
        rst2pdf = RstToPdf()
        rst2pdf.createPdf(doctree=doctree, output=buff)
        return buff.getvalue()

    if  fmt in DOCUTILS_WRITER_NAMES:
        if fmt == 'odt':
            fmt = 'odf_odt'  # Docutils writer name
        if fmt in ('txt', 'rst'):
            return gen_rst(doctree, 0)
        return publish_from_doctree(
            doctree,
            writer_name=fmt,
            settings_overrides=dt_settings
        )
    else:
        raise Exception('Format not supported. Not in %s' % (
                SUPPORTED_FORMATS,
            )
        )


def get_model_for_path(path):
    '''
    Returns a django.db.models.Model instance
    `path`: string with ``app_label.ModelName``
    '''
    app_name, model_name = path.split('.')
    return models.get_model(app_name, model_name)


def get_model_attr_recursive(obj,attr):
    try:
        return getattr(obj,attr),True
    except AttributeError:
        tokens = attr.split('.')
        if len(tokens) > 1:
            return get_model_attr_recursive(
                getattr(obj,tokens[0]),str.join('.',tokens[1:])
            )
        else:
            return False,False


def get_values_for_obj_field(obj, field, mapped=True):
    if field:
        field_is_related = field.find('.') > 0
        if not field_is_related:
            return getattr(obj, field)
        else:
            try:
                return get_model_attr_recursive(obj, field)[0] or ''
            except:
                results = []
                related_field_name = '.'.join(field.split('.')[1:])
                related_name = field.split('.')[0] + '_set'
                for related_obj in getattr(obj, related_name).all():
                    value = get_values_for_obj_field(
                        related_obj,
                        related_field_name,
                        mapped
                    )
                    if isinstance(value, Iterable):
                        results += value
                    else:
                        results.append(value)
                return results
    else:
        return obj


def ireport_factory(slug):
    '''
    Returns an IReport instance, the DBR's internal report representation.
    '''

    messages_list = []

    rep = Report.objects.get(slug=slug)

    rep_model = get_model_for_path(rep.model)

    columns_q = Column.objects.filter(report=rep).order_by('id')

    fields = [x.field for x in columns_q]
    columns = [
        {
            'title': x.label or x.field,
            'width': x.width
        }
        for x in columns_q
    ]

    customcolumns_q = CustomColumn.objects.filter(report=rep)
    for custom_column in customcolumns_q:
        columns.append(
            {
                'title': custom_column.label,
                'width': custom_column.width,
            }
        )

    annotations = Annotate.objects.filter(report=rep)
    annotations = [(x.field, x.function) for x in annotations]

    filters = get_filters_for_report(rep.id)
    excludes = filters['excludes']
    filters = filters['filters']

    groupings = GroupBy.objects.filter(report=rep)
    groupings = [x.field for x in groupings]

    charts = Chart.objects.filter(report=rep)
    charts = [
        {
            'id': x.id,
            'field': x.field,
            'uri': 'http://%s%s' % (
                Site.objects.get_current().domain,
                x.get_absolute_url()
            ),
            'description': x.description,
        }
        for x in charts
    ]

    ireport_attrs = {
        'title': rep.title,
        'description': rep.description,
        'columns': columns,
        'annotations': annotations,
        'filters': filters,
        'excludes': excludes,
        'groupings': groupings,
        'charts': charts,
    }

    report_rows = [
        [
            get_values_for_obj_field(obj, attr)
            for attr in [ '.'.join(f.split('.')[2:]) for f in fields ]
        ]
        for obj in filter_data(rep.id, rep_model)
    ]

    cc_eval_env = {
        '__builtins__': [],
    }

    cc_cache = {}

    if customcolumns_q:
        for r_row in report_rows:
            # Populate the column's evaluation environment
            for labeled_row in zip(fields, r_row):
                cc_eval_env[labeled_row[0].replace('.', '__')] = labeled_row[1]
            for key, func in CC_AGGREGATION_FUNCS.iteritems():
                cc_eval_env[key] = func
            for custom_column in customcolumns_q:
                # Evaluate the row value
                try:
                    val = eval(custom_column.value.replace('.', '__'), cc_eval_env)
                except:
                    messages_list.append((messages.ERROR, _('Failed to eval custom column %s' % custom_column.label)))
                    val = 0
                # Store the value on our _cache_
                if cc_cache.get(custom_column.label):
                    cc_cache[custom_column.label].append(val)
                else:
                    # New column, first value
                    cc_cache[custom_column.label] = [val, ]
                r_row.append(
                    val
                )

    mapped_rows = [
        [
            {
                'obj' : element,
                'type' :'object'
            } if not isinstance(element, list)
            else {
                'obj' : element,
                'type' : 'iterable'
            }
            for element in row
        ]
        for row in report_rows
    ]

    ireport_attrs['rows'] = mapped_rows

    aggregations_q = Aggregate.objects.filter(report=rep)
    # It's needed because the `aggregations` attr of the attribute
    # will never be really empty.
    ireport_attrs['has_aggregations'] = aggregations_q and True or False
    aggregations = []
    for field in fields:
        tmp = None
        for aggr in aggregations_q:
            if aggr.field == field:
                db_models = importlib.import_module('django.db.models')
                function = getattr(db_models, aggr.function)
                try:
                    tmp = (
                        # Apply the aggregation function to a flattened list of values
                        CC_AGGREGATION_FUNCS[aggr.function](
                            [
                                item
                                for iter_ in
                                [
                                    get_values_for_obj_field(obj, '.'.join(field.split('.')[2:]), False)
                                    for obj in filter_data(rep.id, rep_model)
                                ]
                                for item in iter_
                            ]
                        ),
                        FUNCTION_NAMES_MAP[aggr.function]
                    )
                except:
                    messages_list.append(
                        (
                            messages.ERROR,
                            _('Failed to aggregate %s with function %s' % (
                                aggr.field, FUNCTION_NAMES_MAP[aggr.function]
                            )
                          )
                        )
                    )
                    tmp = (0, FUNCTION_NAMES_MAP[aggr.function])
        aggregations.append(tmp)
    for custom_column in customcolumns_q:
        tmp = None
        if custom_column.aggregation:
            func = CC_AGGREGATION_FUNCS[custom_column.aggregation]
            column = cc_cache[custom_column.label]
            try:
                tmp = (
                    func(column),
                    FUNCTION_NAMES_MAP[custom_column.aggregation]
                )
            except:
                messages_list.append(
                    (
                        messages.ERROR,
                        _('Failed to aggregate %s with function %s' % (
                            custom_column.label,
                            FUNCTION_NAMES_MAP[custom_column.aggregation]
                        )
                      )
                    )
                )
                tmp = (0, FUNCTION_NAMES_MAP[custom_column.aggregation])
        aggregations.append(tmp)
    ireport_attrs['aggregations'] = aggregations

    if groupings:
        for group_name in groupings:
            group_rel_obj = getattr(rep_model, '%s' % group_name)
            group_field = getattr(group_rel_obj, 'field')
            gchoice_key = 'grouping_choices_%s' % group_name
            ireport_attrs[gchoice_key] = group_field.get_choices()[1:]
            for ind, opt in ireport_attrs['grouping_choices_%s' % group_name]:
                # FIXME: There's a lot of duplication here.
                group_filters = {}
                group_filters[group_name] = ind
                for filt in filters:
                    group_filters['%s%s' % filt[0:2]] = filt[3]
                group_rows = [
                    [
                        hasattr(obj, attr) if getattr(
                            obj,
                            attr
                        ) else getattr(obj, attr + '_set')
                        for attr in fields
                    ]
                    for obj in rep_model.objects.filter(**group_filters)
                ]
                group_cc_eval_env = {
                    '__builtins__': [],
                }

                group_cc_cache = {}
                if customcolumns_q:
                    for r_row in group_rows:
                        for labeled_row in zip(fields, r_row):
                            group_cc_eval_env[labeled_row[0]] = labeled_row[1]
                        for cc in customcolumns_q:
                            try:
                                val = eval(custom_column.value, group_cc_eval_env)
                            except:
                                messages_list.append((messages.ERROR, _('Failed to eval custom column %s' % custom_column.label)))
                                val = 0
                            # Store the column on our _cache_
                            if group_cc_cache.get(custom_column.label):
                                group_cc_cache[custom_column.label].append(val)
                            else:
                                # New column, first value
                                group_cc_cache[custom_column.label] = [val, ]
                            r_row.append(
                                val
                            )
                ireport_attrs['rows_%s' % opt] = group_rows
                group_aggregations = []
                for field in fields:
                    tmp = None
                    for aggr in aggregations_q:
                        if aggr.field == field:
                            db_m = importlib.import_module('django.db.models')
                            function = getattr(db_m, aggr.function)
                            try:
                                tmp = (
                                    rep_model.objects.filter(
                                        **group_filters
                                    ).aggregate(foo=function(aggr.field))['foo'],
                                    FUNCTION_NAMES_MAP[aggr.function]
                                )
                            except:
                                messages_list.append(
                                    (
                                        messages.ERROR,
                                        _('Failed to aggregate %s with function %s' % (
                                            aggr.field, FUNCTION_NAMES_MAP[aggr.function]
                                        )
                                      )
                                    )
                                )
                                tmp = (0, FUNCTION_NAMES_MAP[aggr.function])
                    group_aggregations.append(tmp)
                for custom_column in customcolumns_q:
                    tmp = None
                    if custom_column.aggregation:
                        func = CC_AGGREGATION_FUNCS[custom_column.aggregation]
                        column = group_cc_cache[custom_column.label]
                        try:
                            tmp = (
                                func(column),
                                FUNCTION_NAMES_MAP[custom_column.aggregation]
                            )
                        except:
                            messages_list.append(
                                (
                                    messages.ERROR,
                                    _('Failed to aggregate %s with function %s' % (
                                        custom_column.label,
                                        FUNCTION_NAMES_MAP[custom_column.aggregation]
                                    )
                                  )
                                )
                            )
                            tmp = (0, FUNCTION_NAMES_MAP[custom_column.aggregation])
                    group_aggregations.append(tmp)
                ireport_attrs['aggregations_%s' % opt] = group_aggregations

    ireport_cls = type(
        'IReport',
        (object, ),
        ireport_attrs,
    )

    return ireport_cls(), messages_list


def get_filters_for_report(rep_id):
    filters_q = Filter.objects.filter(report__id=rep_id)
    filters = []
    excludes = []
    for filt in filters_q:
        filter_value = str(filt.value)
        if filt.exclude:
            excludes.append(
                (
                    filt.column,
                    filt.operator,
                    filt.operator_short,
                    filter_value
                )
            )
        else:
            filters.append(
                (
                    filt.column,
                    filt.operator,
                    filt.operator_short,
                    filter_value
                )
            )
    return {'filters': filters, 'excludes': excludes}


def filter_data(rep_id, rep_model):
    filters = get_filters_for_report(rep_id)
    rows_filters = {}
    for filt in filters['filters']:
        field_name = '.'.join(filt[0].split('.')[2:]).replace('.', '__')
        filter_oper = filt[1]
        filter_value = str(filt[3])
        rows_filters['%s%s' % (field_name, filter_oper)] = filter_value
    rows_excludes = {}
    for excl in filters['excludes']:
        field_name = '.'.join(excl[0].split('.')[2:]).replace('.', '__')
        exclude_oper = excl[1]
        exclude_value = str(excl[3])
        rows_excludes['%s%s' % (field_name, exclude_oper)] = exclude_value
    objects = rep_model.objects.filter(**rows_filters)
    objects = objects.exclude(**rows_excludes)
    return objects
