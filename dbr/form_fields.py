from django.forms.fields import CharField, MultiValueField

from dbr.widgets import DbrModelFieldWidget, DbrHiddenModelFieldWidget


class DbrModelFieldFormField(MultiValueField):

    widget = DbrModelFieldWidget

    hidden_widget = DbrHiddenModelFieldWidget

    def __init__(self, *args, **kwargs):
        default_fields = (
            CharField(max_length=480),
            CharField(max_length=20)
        )
        super(DbrModelFieldFormField, self).__init__(
            fields=default_fields, *args, **kwargs
        )

    def compress(self, data):
        if data:
            c_data = (data[0] or '', data[1] or '')
            return ','.join(c_data)
        return None

