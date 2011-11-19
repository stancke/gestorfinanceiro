from django import forms

from dbr.models import Report

class InitialReportPropertiesForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ('slug', )

