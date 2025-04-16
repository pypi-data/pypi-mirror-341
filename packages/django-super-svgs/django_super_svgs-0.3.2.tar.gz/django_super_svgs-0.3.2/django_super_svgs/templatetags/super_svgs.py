from django import template

from .base import RenderSvg

register = template.Library()


@register.tag
def svg(parser, token):
    """Return a choosen svg rendered."""
    return RenderSvg(parser=parser, token=token)


@register.filter
def split(value, separator=","):
    """Split a string by a separator."""
    return value.split(separator)
