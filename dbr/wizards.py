from django.contrib.formtools.wizard import FormWizard
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.encoding import force_unicode

from dbr.models import Report

class ReportCreationWizard(FormWizard):
    '''
    Simple wizard to guide the user over the creation of a report
    '''

    # It needs a __name__
    # http://elo80ka.wordpress.com/2009/10/28/using-a-formwizard-in-the-django-admin/
    @property
    def __name__(self):
        return self.__class__.__name__

    # To change the default 'forms/wizard.html'
    def get_template(self, step):
        return 'dbr/wizards/report.html'

    # Override parse_params to fill the template context
    def parse_params(self, request, admin=None, *args, **kwargs):
        self._model_admin = admin
        opts = admin.model._meta
        self.extra_context.update({
            'title': u'Add %s' % force_unicode(opts.verbose_name),
            'current_app': admin.admin_site.name,
            'has_change_permission': admin.has_change_permission(request),
            'add': True,
            'opts': opts,
            'root_path': admin.admin_site.root_path,
            'app_label': opts.app_label,
        })

    # Define the actions to take when the wizard is done
    def done(self, request, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        report = Report(
            title = data['title'],
            description = data['description'],
            is_public = data['is_public'],
            model = data['model']
        )
        report.save()

        return HttpResponseRedirect(
            reverse(
                'admin:dbr_report_change',
                args=[report.id]
            )
        )
