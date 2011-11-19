from django.db import models
from django.utils.translation import ugettext_lazy as _

from dbr.form_fields import DbrModelFieldFormField
from dbr.widgets import DbrModelAttrWidget, DbrSimpleModelFieldWidget

# South migration compatability for our custom field(s)
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^dbr\.fields\.DbrModelAttrField'])
    add_introspection_rules([], ['^dbr\.fields\.DbrModelFieldField'])
    add_introspection_rules([], ['^dbr\.fields\.DbrSimpleModelFieldField'])
except ImportError:
    pass


# Get all available model fields
def model_fields_choices():
    return tuple(
        [
            (
                model_._meta.object_name,
                tuple(
                    [
                        (field_name, field_name)
                        for field_name in model_._meta.get_all_field_names()
                    ]
                )
            )
            for model_ in models.get_models()
        ]
    )

get_fields_or_recurse = lambda field_desc: {
    'name': field_desc[0].name,
    'model': '%s.%s' % (
        field_desc[0].rel.to._meta.app_label,
        field_desc[0].rel.to._meta.object_name
    ),
    'type': 'related',
    'fields': [
        {
            'name': fn,
            'type': 'direct'
        }
        for fn in
        field_desc[0].rel.to._meta.get_all_field_names()
    ]
} if isinstance(
    field_desc[0],
    models.ForeignKey
) else (
    {
        'name': field_desc[0].name,
        'type': 'direct',
    } if isinstance(
        field_desc[0], models.Field
    )
    else (
        {
            'name': field_desc[0].var_name,
            'model': '%s.%s' % (
                field_desc[0].model._meta.app_label,
                field_desc[0].model._meta.object_name
            ),
            'type': 'related',
            'fields': model_fields_tree(
                field_desc[0].model
            )
        }
    )
)

def model_fields_tree(model):
    '''
    Recursively gets all fields of a model and all fields of its
    related objects and returns a list of nested dicts with structure::
        [
            {
                'name' : field_name,
                'type' : 'direct', # For Field instances
            },
            {
                'name' : related_object_var_name,
                'type' : 'related', # For RelatedObject instances
                'fields' : {
                     ...
                }
            }
        ]
    '''
    fields = [
        model._meta.get_field_by_name(fn)
        for fn in model._meta.get_all_field_names()
    ]
    return map(get_fields_or_recurse, fields)


def model_fields_tree_flat(tree, model_name=''):
    yield model_name
    model_name += '.'
    for leaf in tree:
        if leaf['type'] == 'direct':
            yield model_name + leaf['name']
        else:
            for i in list(
                model_fields_tree_flat(
                    leaf['fields'],
                    model_name + leaf['name']
                )
            ):
                yield(i)


class DbrModelAttrField(models.CharField):

    description = _('Model attribute selector')

    def __init__(self, *args, **kwargs):
        # Force choices and max_length
        kwargs['choices'] = model_fields_choices()
        kwargs['max_length'] = 250
        if not kwargs.get('verbose_name', None):
            kwargs['verbose_name'] = _('field')

        super(DbrModelAttrField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = DbrModelAttrWidget
        return super(DbrModelAttrField, self).formfield(**kwargs)


class DbrModelFieldField(models.Field):

    __metaclass__ = models.SubfieldBase

    description = _(
        'A DBR specific model field with optional summary function'
    )

    def __init__(self, *args, **kwargs):
        defaults = {
            'max_length': 500,
            'verbose_name': _('model field'),
            'help_text': _(
                'Select a field of the selected model and, '
                'if available, a summary operation for the '
                'value.'
            )
        }
        defaults.update(**kwargs)
        super(DbrModelFieldField, self).__init__(*args, **defaults)

    def db_type(self, connection):
        return 'varchar(%s)' % self.max_length

    def to_python(self, value):
        if value:
            if isinstance(value, (tuple, list)):
                ret = value
            else:
                ret = value.split(',')
        else:
            ret = ['', '']
        return ret

    def get_internal_type(self):
        return 'DbrModelFieldField'

    def get_prep_value(self, value):
        return ','.join(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': DbrModelFieldFormField,
        }
        defaults.update(kwargs)
        return super(DbrModelFieldField, self).formfield(**defaults)

class DbrSimpleModelFieldField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 250
        if not kwargs.get('verbose_name', None):
            kwargs['verbose_name'] = _('field')

        super(DbrSimpleModelFieldField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = DbrSimpleModelFieldWidget
        return super(DbrSimpleModelFieldField, self).formfield(**kwargs)
