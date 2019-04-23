from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag
def moban(a1,a2):
    return a1+a2