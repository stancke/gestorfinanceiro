from django import forms
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.utils.functional import update_wrapper
from django.utils.translation import ugettext as _

from dbr.models import (Column, CustomColumn, Annotate, Aggregate, GroupBy,
                        Filter, Chart, Report)
from dbr.forms import InitialReportPropertiesForm
from dbr.wizards import ReportCreationWizard


class ColumnInline(admin.StackedInline):
    model = Column
    extra = 1


class CustomColumnForm(forms.ModelForm):
    class Meta:
        model = CustomColumn

    def clean(self):
        value = self.cleaned_data['value']

        invalid_msg = _(
            'There are syntax errors in the column\'s value. '
            'Please fix it to save the report.'
        )

        try:
            eval(value)
        except NameError:
            # We don't want to catch NameErrors because
            # the cell values are still unknown
            pass
        except SyntaxError:
            self._errors['value'] = self.error_class([invalid_msg])
            del self.cleaned_data['value']
        except:
            pass
        return self.cleaned_data


class CustomColumnInline(admin.StackedInline):
    model = CustomColumn
    form = CustomColumnForm
    extra = 0


class AnnotateInline(admin.StackedInline):
    model = Annotate
    extra = 1


class AggregateInline(admin.StackedInline):
    model = Aggregate
    extra = 1


class GroupByInline(admin.StackedInline):
    model = GroupBy
    extra = 1


class FilterInline(admin.StackedInline):
    model = Filter
    extra = 1


class ChartInline(admin.StackedInline):
    model = Chart
    extra = 0


def view_report(self):
    return u'<a href="%s">%s</a>' % (
        self.get_absolute_url(),
        unicode(_('View'))
    )
view_report.short_description = (unicode(_('View report')))
view_report.allow_tags = True


class ReportAdmin(admin.ModelAdmin):
    '''
    Report admin description
    '''

    list_display = ['title', 'model', 'is_public', view_report]
    list_display_links = ['title']
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = ('title',)
    list_filter = ('is_public',)
    list_editable = ('is_public',)
    date_hierarchy = 'created'
    inlines = [
        ColumnInline,
        CustomColumnInline,
        AggregateInline,
        # GroupByInline,
        FilterInline,
        ChartInline,
    ]

    class Media:
        js = (
            'dbr/js/widgets/dbr-simple-model-field-widget.js',
        )

    # It's needed to override the default ^add/$ view
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwds):
                kwds['admin'] = self   # Use a closure to pass this admin instance to our wizard
                return self.admin_site.admin_view(view)(*args, **kwds)
            return update_wrapper(wrapper, view)
        urlpatterns = patterns(
            '',
            url(
                r'^add/$',
                wrap(ReportCreationWizard([InitialReportPropertiesForm,])),
                name='dbr_report_add'
            ),
        ) + super(ReportAdmin, self).get_urls()
        return urlpatterns


admin.site.register(Report, ReportAdmin)
