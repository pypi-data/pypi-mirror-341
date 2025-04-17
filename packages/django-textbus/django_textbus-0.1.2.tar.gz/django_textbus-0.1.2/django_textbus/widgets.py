import json
from django import forms
from django.conf import settings
from django.forms.widgets import Media
from django.utils.safestring import mark_safe

from .conf import TEXTBUS_CONFIG


class TextbusWidget(forms.Textarea):
    """
    Textbus富文本编辑器的Django表单小部件
    """
    template_name = 'django_textbus/widget.html'

    def __init__(self, attrs=None, config=None):
        default_attrs = {'class': 'textbus-editor'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        self.config = config or TEXTBUS_CONFIG

    @property
    def media(self):
        """
        返回Textbus编辑器所需的JS和CSS文件
        """
        js = [
            'django_textbus/js/textbus.js',
            'django_textbus/js/textbus-init.js',
        ]
        css = {
            'all': [
                'django_textbus/css/textbus.css',
                'django_textbus/css/textbus-theme.css',
            ]
        }
        return Media(js=js, css=css)

    def get_context(self, name, value, attrs):
        """
        添加Textbus配置到模板上下文
        """
        context = super().get_context(name, value, attrs)
        context['widget']['config'] = self.config
        context['widget']['config_json'] = mark_safe(json.dumps(self.config))
        return context
