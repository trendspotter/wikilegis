# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.template import Library
from django.utils.text import force_text
from django.forms import widgets
from . import _utils


register = Library()


@register.simple_tag
def render_field(field, *args, **kwargs):
    extra_classes = kwargs.pop('extra_classes', [])
    extra_classes = _utils.parse_extra_classes(extra_classes)

    widget = kwargs.pop('widget', None)
    if widget is not None:
        if isinstance(widget, basestring):
            widget_name = widget
            widget = getattr(widgets, widget_name, None)
            assert widget, NameError("Undefined widget: '{0}'".format(widget_name))
            widget = widget()

    attrs = {
        'class': ' '.join(extra_classes),
    }

    return field.as_widget(widget=widget, attrs=attrs)


@register.simple_tag
def render_materialized_field(field, *args, **kwargs):
    extra_classes = kwargs.pop('extra_classes', [])
    extra_classes = _utils.parse_extra_classes(extra_classes)

    if field.errors:
        extra_classes.append('invalid')

    kwargs['extra_classes'] = extra_classes

    field_errors = force_text(field.errors) if field.errors else ''

    return '\n'.join([
        render_field(field, *args, **kwargs),
        field.label_tag(),
        field_errors,
    ])
