from widget_tweaks.templatetags.widget_tweaks import add_class
from django import template


register = template.Library()


def add_class_validations(field, args):
    if field.errors:
        # Use add class from widget tweaks rather then recreating the whole
        # thing
        return add_class(field, args)
    return field


register.filter("add_class_validations", add_class_validations)
