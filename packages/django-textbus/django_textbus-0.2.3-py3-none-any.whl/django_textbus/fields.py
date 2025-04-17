from django.db import models
from django.forms import fields

from .widgets import TextbusWidget


class TextbusFormField(fields.CharField):
    """
    Textbus富文本编辑器的表单字段
    """
    def __init__(self, config=None, *args, **kwargs):
        kwargs['widget'] = TextbusWidget(config=config)
        super().__init__(*args, **kwargs)


class TextbusField(models.TextField):
    """
    Textbus富文本编辑器的模型字段
    """
    description = "Textbus富文本字段"
    
    def __init__(self, config=None, *args, **kwargs):
        self.config = config
        super().__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': TextbusFormField,
            'config': self.config,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
