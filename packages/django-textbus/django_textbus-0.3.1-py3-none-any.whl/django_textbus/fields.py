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

    def clean(self, value):
        """
        清理和验证表单字段值
        """
        # 如果值是"None"字符串，则返回空字符串
        if value == "None" or value == "undefined":
            value = ""
        return super().clean(value)


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

    def get_prep_value(self, value):
        """
        在存储到数据库前处理值
        """
        # 如果值是"None"字符串，则返回空字符串
        if value == "None" or value == "undefined":
            return ""
        return super().get_prep_value(value)

    def to_python(self, value):
        """
        将数据库值转换为Python对象
        """
        # 如果值是None或"None"，则返回空字符串
        if value is None or value == "None" or value == "undefined":
            return ""
        return super().to_python(value)
