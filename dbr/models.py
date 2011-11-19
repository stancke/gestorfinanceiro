# -*- coding: utf-8 -*-
'''
Django Business Reports data models definition
'''

from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from dbr.fields import DbrSimpleModelFieldField

MODEL_CHOICES = [
    (
        model._meta.app_label + '.' + model._meta.object_name,
        model._meta.app_label + '.' + model._meta.object_name,
    )
    for model in models.get_models()
]

CHART_TYPE_CHOICES = (
#    ('PieChart', _('Pie Chart')),
    ('VerticalBarChart', _('Barra Vertical')),
    ('HorizontalBarChart', _('Barra Horizontal')),
    ('LineChart', _('Linha')),
)

# Palette based on http://modernl.com/article/web-2.0-colour-palette
CHART_COLOR_PALETTE = (
    ('#000000', _('Preto')),
    ('#EEEEEE', _('Prata')),
    ('#C79810', _('Ouro')),
    ('#C3D9FF', _('Azul Claro')),
    ('#0000FF', _('Azul')),
    ('#3F4C6B', _('Azul Escuro')),
    ('#CDEB8B', _('Verde Claro')),
    ('#008C00', _('Verde')),
    ('#006E2E', _('Verde Escuro')),
    ('#FFFF88', _('Amarelo')),
    ('#FF1A00', _('Vermelho')),
    ('#B02B2C', _('Vermelho Escuro')),
    ('#FF7400', _('Laranja')),
)

FUNCTION_CHOICES = (
    ('Sum', _('Sum')),
    ('Count', _('Count')),
    ('Avg', _('Average')),
    ('Max', _('Maximum')),
    ('Min', _('Minimum')),
    ('StdDev', _('Standard Deviation')),
    ('Variance', _('Variance')),
)

FILTER_OPERATOR_CHOICES = (
    ('__iexact', _('Igual')),
    ('__icontains', _('Contem')),
    ('__in', _('Existe em lista (comma separated)')),
    ('__gt', _('Maior que')),
    ('__gte', _('Maior ou igual que')),
    ('__lt', _('Menor que')),
    ('__lte', _('Menor ou igual que')),
    ('__istartswith', _('Comeca com')),
    ('__iendswith', _('Termina com')),
    ('__range', _('Entre (comma separated bounds)')),
    ('__year', _('Ano (only date fields)')),
    ('__month', _('Mes (only date fields)')),
    ('__day', _('Day (only date fields)')),
    ('__week_day', _('Week day (only date fields)')),
    ('__iregex', _('Regular expression'))
)

SHORT_OPER_MAP = {
    '__iexact': '=',
    '__icontains': unicode(_('contains')),
    '__in': unicode(_('in')),
    '__gt': '>',
    '__gte': '>=',
    '__lt': '<',
    '__lte': '<=',
    '__istartswith': unicode(_('start')),
    '__iendswith': unicode(_('end')),
    '__range': unicode(_('between')),
    '__year': unicode(_('year =')),
    '__month': unicode(_('month =')),
    '__day': unicode(_('day =')),
    '__week_day': unicode(_('week day =')),
    '__iregex': unicode(_('matches')),
}


class Report(models.Model):
    '''
    Report persistance description
    '''
    title = models.CharField(_('titulo'), max_length=180)
    description = models.TextField(_('descricao'))
    slug = models.SlugField(_('slug'), blank=True, unique=True)
    is_public = models.BooleanField(_('publico?'), default=False)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)
    model = models.CharField(
        _('model'),
        max_length=250,
        choices=MODEL_CHOICES,
        help_text=_('Select the database model from which'
                    ' the data will be extracted'),
    )

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.id:
            self.created = datetime.today()
        self.updated = datetime.today()
        self.slug = slugify(self.title)
        super(Report, self).save()

    @models.permalink
    def get_absolute_url(self):
        '''
        Returns the absolute URL of the report's view
        '''
        return ('dbr-view', (), {'slug': self.slug})


class Column(models.Model):
    '''
    Data representation of a report's column
    '''
    report = models.ForeignKey('Report')
    field = DbrSimpleModelFieldField()
    label = models.CharField(
        _('label'),
        blank=True,
        max_length=50,
        help_text=_('Alternative label for the column'),
    )
    width = models.CharField(
        _('width'),
        max_length=3,
        help_text=_('The width of the column in percentage')
    )

    def __unicode__(self):
        return self.field

    class Meta:
        verbose_name = _('column')
        verbose_name_plural = _('columns')


class CustomColumn(models.Model):
    '''
    Generic model to define complimentary non field related columns
    '''
    report = models.ForeignKey('Report')
    label = models.CharField(
        _('label'),
        max_length=20,
        help_text=_('Custom column\'s title and identifier.'),
    )
    identifier = models.CharField(
        _('identifier'),
        max_length=20,
        help_text=_(
            'Identifier for the custom column in filters and other evaluations'
        ),
    )
    value = models.CharField(
        _('value'),
        max_length=200,
        help_text=_(
            'Value for the custom column.'
            ' Available variables are the other column values.'
            ' It can perform basic mathematics operations.'
        ),
    )
    width = models.CharField(
        _('width'),
        max_length=3,
        help_text=_('Custom column percentage width in the report\'s view.')
    )
    aggregation = models.CharField(
        _('aggregation'),
        max_length=20,
        choices=FUNCTION_CHOICES,
        blank=True,
        help_text=_('Optional aggregation for the custom column')
    )

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = _('custom column')
        verbose_name_plural = _('custom columns')


class Annotate(models.Model):
    '''
    Definition of annotations for the report's items
    '''
    report = models.ForeignKey('Report')
    field = DbrSimpleModelFieldField()
    function = models.CharField(
        _('function'),
        max_length=20,
        choices=FUNCTION_CHOICES
    )

    def __unicode__(self):
        return self.field

    class Meta:
        verbose_name = _('annotate')
        verbose_name_plural = _('annotates')


class Aggregate(models.Model):
    '''
    Definition of aggregations for report's columns
    '''
    report = models.ForeignKey('Report')
    field = DbrSimpleModelFieldField()
    function = models.CharField(
        _('function'),
        max_length=20,
        choices=FUNCTION_CHOICES
    )

    def __unicode__(self):
        return self.field

    class Meta:
        verbose_name = _('aggregate')
        verbose_name_plural = _('aggregates')


class Filter(models.Model):
    '''
    Filter:
    -------

    Defines a restriction over the data on te report

    `column`: attribute to filter out with `value`.
    `operator`: operation to apply over `column`.
    `value`: the value of the filter. It's applied by simple substitution and
    evaluation.
    Available functions are the same ones than for annotations and aggregations
    '''

    report = models.ForeignKey('Report')
    column = DbrSimpleModelFieldField()
    operator = models.CharField(
        _('operator'),
        max_length=20,
        choices=FILTER_OPERATOR_CHOICES
    )
    operator_short = models.CharField(
        max_length=20,
        editable=False
    )
    value = models.CharField(
        _('value'),
        max_length=250,
    )
    exclude = models.BooleanField(
        help_text=_('If set, will exclude all data matching the filter.')
    )

    def __unicode__(self):
        return self.column

    def save(self):
        self.operator_short = SHORT_OPER_MAP[self.operator]
        super(Filter, self).save()

    class Meta:
        verbose_name = _('filter')
        verbose_name_plural = _('filters')


class GroupBy(models.Model):
    '''
    Grouping data model
    '''
    report = models.ForeignKey('Report', related_name='groupby')
    field = DbrSimpleModelFieldField()

    def __unicode__(self):
        return self.field

    class Meta:
        verbose_name = _('group by')
        verbose_name_plural = _('groupings')


class Chart(models.Model):
    '''
    Data model for charts in reports
    '''
    report = models.ForeignKey('Report')
    chart_type = models.CharField(
        _('chart type'),
        max_length=30,
        choices=CHART_TYPE_CHOICES
    )
    field = DbrSimpleModelFieldField(help_text=_('Column to display in the chart'))
    color = models.CharField(
        _('color'),
        max_length=20,
        choices=CHART_COLOR_PALETTE,
        default='#000000',
        help_text=_('Color of the bars or lines')
    )
    label = models.CharField(
        _('label'),
        max_length=160,
        help_text=_('Axis label. Defaults to the report\'s model name'),
        blank=True
    )
    element_tag = DbrSimpleModelFieldField(
        verbose_name=_('element tag'),
        help_text=_(
            'Model field to use as identifier for every element in the chart. '
            'Defaults to the object id.'
        ),
        blank=True
    )
    description = models.TextField(
        _('description'),
        blank=True
    )

    def __unicode__(self):
        return self.field

    @models.permalink
    def get_absolute_url(self):
        '''
        Returns the absolute URL of the chart
        '''
        return ('dbr-view-chart', (), {'chart_id': self.id})

    class Meta:
        verbose_name = _('chart')
        verbose_name_plural = _('charts')
