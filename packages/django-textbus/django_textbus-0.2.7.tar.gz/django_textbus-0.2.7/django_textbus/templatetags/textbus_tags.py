from django import template
from django.utils.safestring import mark_safe
from django_textbus.widgets import TextbusWidget

register = template.Library()


@register.simple_tag
def textbus_css():
    """
    返回Textbus编辑器所需的CSS文件
    """
    widget = TextbusWidget()
    return mark_safe('\n'.join(['<link href="%s" type="text/css" media="%s" rel="stylesheet" />' % (path, media) 
                               for path, media in widget.media._css.items()]))


@register.simple_tag
def textbus_js():
    """
    返回Textbus编辑器所需的JS文件
    """
    widget = TextbusWidget()
    return mark_safe('\n'.join(['<script type="text/javascript" src="%s"></script>' % path 
                               for path in widget.media._js]))
