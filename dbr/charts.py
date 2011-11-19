'''
Django Business Reports charting module
'''

from cStringIO import StringIO

import cairo
from pycha.line import LineChart
from pycha.bar import VerticalBarChart, HorizontalBarChart
from pycha.pie import PieChart

from django.contrib.auth.decorators import login_required
from django.db.models import get_model
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from dbr.core import filter_data, get_values_for_obj_field
from dbr.models import Chart, Filter


def chart_factory(
    dataset,
    chart_type='LineChart',
    opts={},
    width=800,
    height=520
    ):
    obuff = StringIO()

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    chart = globals()[chart_type](surface, options=opts)
    chart.addDataset(dataset)
    chart.render()

    surface.write_to_png(obuff)

    del chart
    del surface

    return obuff.getvalue()

@login_required
def chart_view(request, chart_id):
    errors = []

    chart_model = Chart.objects.get(id=chart_id)

    module_name, model_name = chart_model.report.model.split('.')

    rep_model = get_model(module_name, model_name)

    model_data = filter_data(
        chart_model.report.id,
        rep_model
    )

    try:
        dataset = (
            chart_model.field,
            tuple(
                [
                    (
                        e[0],
                        float(
                            get_values_for_obj_field(
                                e[1],
                                '.'.join(chart_model.field.split('.')[2:])
                            )
                        )
                    )
                    for e in enumerate(model_data)
                ]
            )
        ),  # Don't erase the comma
    except TypeError:
        dataset = (chart_model.field, ((0,0),)),
        errors.append(_('Failed to generate dataset with given field'))

    xlabels = [
        str(get_values_for_obj_field(e, '.'.join(chart_model.element_tag.split('.')[2:]) or 'id'))
        for e in model_data
    ]

    opts = {
        'axis': {
            'labelFontSize': 12,
            'tickFontSize': 10,
            'x': {
                'ticks': [
                    dict(v=i, label=l)
                    for i, l in enumerate(xlabels)
                ],
                'label': model_name,
                'rotate': 75,
            },
        },
        'background': {
            'hide': True,
        },
        'barWidthFillFraction': 0.65,
        'colorScheme': {
            'name': 'gradient',
            'args': {
                'initialColor': chart_model.color,
            },
        },
        'legend': {
            'hide': len(dataset) == 1 and True or False,
        },
        'padding': {
            'left': 20,
            'right': 20,
            'top': 20,
            'bottom': 20,
        },
        'shouldFill': chart_model.chart_type == 'LineChart' and False or True,
        'title': chart_model.field if not errors else '\n'.join(
            [unicode(e) for e in errors]
        ),
        'titleFontSize': 14,
        'yvals': {
            'fontSize': 8,
            'show': True,
        },
    }

    response = HttpResponse(mimetype='image/png')
    chart_img = chart_factory(
        dataset,
        chart_type=chart_model.chart_type,
        opts=opts,
    )
    response['Content-Length'] = str(len(chart_img))
    response.write(chart_img)

    return response
