# Needed to get the URL of the AJAX view used to get model fields
from django.core.urlresolvers import reverse
from django.forms.widgets import Select, MultiWidget


class DbrModelAttrWidget(Select):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'dbr-model-attr'
        super(DbrModelAttrWidget, self).__init__(attrs)


FORMAT_CHOICES = (
    ('', '')
)

class DbrModelFieldWidget(MultiWidget):

    def __init__(self, attrs=None):
        attrs = attrs or {}
        field_attrs = {
            'class': 'dbr-model-fields-choice',
            'data-fields-options-url': reverse('dbr-model-fields-json'),
            'data-summary-options-url': reverse('dbr-field-summary-opts-json'),
        }
        field_attrs.update(**attrs)
        format_attrs = {
            'class': 'dbr-model-fields-format',
 #           'style': 'display: none;'
        }
        format_attrs.update(**attrs)
        widgets = (
            Select(attrs=field_attrs), #, choices=self.get_field_choices()),
            Select(attrs=format_attrs, choices=FORMAT_CHOICES),
        )
        super(DbrModelFieldWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return ['', '']

    def value_from_datadict(self, data, files, name):
        try:
            val1 = data.get(name + '_0', '')
            val2 = data.get(name + '_1', '')
            ret = [val1, val2]
            return ret
        except AttributeError:
            ret = [
                widget.value_from_datadict(data, files, name + '_%s' % i)
                for i, widget in
                enumerate(self.widgets)
            ]
            return ret

    class Media:
        js = (
#            'dbr/js/widgets/dbr-model-field-widget.js',
        )

class DbrHiddenModelFieldWidget(DbrModelFieldWidget):
    is_hidden = True

    def __init__(self, attrs=None):
        super(DbrHiddenModelFieldWidget).__init__(self, attrs)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True

class DbrSimpleModelFieldWidget(Select):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'dbr-model-field-select'
        attrs['data-fields-options-url'] = reverse('dbr-model-fields-json')
        super(DbrSimpleModelFieldWidget, self).__init__(attrs)

    # class Media:
    #     js = (
    #         'dbr/js/widgets/dbr-simple-model-field-widget.js',
    #     )
