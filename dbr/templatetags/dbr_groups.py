'''
Grouping related templatetags for `django-business-reports`
'''

import re

from django.template import Library, Node, TemplateSyntaxError, Variable

register = Library()


class DbrChoicesForGrouping(Node):
    '''
    Node used to set grouping choices in the template context
    '''
    def __init__(self, group_name, var_name):
        self.group_name = Variable(group_name)
        self.var_name = var_name
        super(DbrChoicesForGrouping, self).__init__()

    def render(self, context):
        report = context['report']
        choices = getattr(
            report,
            'grouping_choices_' + self.group_name.resolve(context)
        )
        context[self.var_name] = choices
        return ''


def dbr_choices_for_grouping(parser, token):
    '''
    Gets the available choices for a report grouping as a context variable
    '''
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError(
            (
                '%r requires  arguments. Example: '
                'dbr_choices_for_grouping group_name as group_choices'
            ) % token.contents.split()[0]
        )
    args_match = re.search(r'(.*?) as (\w+)', arg)
    if not args_match:
        raise TemplateSyntaxError(
            (
                '%r has invalid arguments. Example: '
                'dbr_choices_for_grouping group_name as group_choices'
            ) % tag_name
        )
    group_name, var_name = args_match.groups()
    return DbrChoicesForGrouping(group_name, var_name)

register.tag('dbr_choices_for_grouping', dbr_choices_for_grouping)


class DbrRowsForGroupChoice(Node):
    '''
    Node used to store group rows specific to a choice in a template context
    '''
    def __init__(self, choice_name, var_name):
        self.choice_name = Variable(choice_name)
        self.var_name = var_name
        super(DbrRowsForGroupChoice, self).__init__()

    def render(self, context):
        report = context['report']
        rows = getattr(
            report,
            'rows_' + self.choice_name.resolve(context)
        )
        context[self.var_name] = rows
        return ''


def dbr_rows_for_gchoice(parser, token):
    '''
    Gets the rows for a group choice and stores it in a context variable
    '''
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError(
            (
                '%r requires  arguments. Example: '
                'dbr_rows_for_group_choice group_name as group_choices'
            ) % token.contents.split()[0]
        )
    args_match = re.search(r'(.*?) as (\w+)', arg)
    if not args_match:
        raise TemplateSyntaxError(
            (
                '%r has invalid arguments. Example: '
                'dbr_rows_for_group_choice group_name as group_choices'
            ) % tag_name
        )
    group_name, var_name = args_match.groups()
    return DbrRowsForGroupChoice(group_name, var_name)

register.tag('dbr_rows_for_group_choice', dbr_rows_for_gchoice)


class DbrAggregationsForGroupChoice(Node):
    '''
    Node used to store aggregations specific to a group choice in a template
    '''
    def __init__(self, choice_name, var_name):
        self.choice_name = Variable(choice_name)
        self.var_name = var_name
        super(DbrAggregationsForGroupChoice, self).__init__()

    def render(self, context):
        report = context['report']
        aggregations = getattr(
            report,
            'aggregations_' + self.choice_name.resolve(context)
        )
        context[self.var_name] = aggregations
        return ''


def dbr_aggrs_for_gchoice(parser, token):
    '''
    Gets the aggregations for a grouping choice and stores it as a context var.
    '''
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError(
            (
                '%r requires  arguments. Example: '
                'dbr_aggregations_for_group_choice group_name as group_choices'
            ) % token.contents.split()[0]
        )
    args_match = re.search(r'(.*?) as (\w+)', arg)
    if not args_match:
        raise TemplateSyntaxError(
            (
                '%r has invalid arguments. Example: '
                'dbr_aggregations_for_group_choice group_name as group_choices'
            ) % tag_name
        )
    group_name, var_name = args_match.groups()
    return DbrAggregationsForGroupChoice(group_name, var_name)

register.tag('dbr_aggregations_for_group_choice', dbr_aggrs_for_gchoice)
