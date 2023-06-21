from django import template

register = template.Library()

@register.filter
def divisibleby(value, arg):
    return value % arg == 0
