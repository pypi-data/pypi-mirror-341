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
        # 打印调试信息
        print(f"TextbusFormField.clean: 原始值 = {repr(value)}, 类型 = {type(value)}")

        # 如果值是None或空字符串或"None"或"undefined"，则返回空字符串
        if value is None or value == "" or value == "None" or value == "undefined":
            print("TextbusFormField.clean: 返回空字符串")
            return ""

        # 确保值是字符串
        if not isinstance(value, str):
            try:
                value = str(value)
                print(f"TextbusFormField.clean: 将非字符串值转换为字符串 = {repr(value)}")
            except Exception as e:
                print(f"TextbusFormField.clean: 转换失败 = {e}")
                return ""

        # 如果值是空白字符串，则返回空字符串
        if value.strip() == "":
            print("TextbusFormField.clean: 值是空白字符串，返回空字符串")
            return ""

        # 调用父类的clean方法
        cleaned_value = super().clean(value)
        print(f"TextbusFormField.clean: 返回清理后的值 = {repr(cleaned_value)}")
        return cleaned_value


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
        # 打印调试信息
        print(f"TextbusField.get_prep_value: 原始值 = {repr(value)}, 类型 = {type(value)}")

        # 如果值是None或空字符串或"None"或"undefined"，则返回空字符串
        if value is None or value == "" or value == "None" or value == "undefined":
            print("TextbusField.get_prep_value: 返回空字符串")
            return ""

        # 确保值是字符串
        if not isinstance(value, str):
            try:
                value = str(value)
                print(f"TextbusField.get_prep_value: 将非字符串值转换为字符串 = {repr(value)}")
            except Exception as e:
                print(f"TextbusField.get_prep_value: 转换失败 = {e}")
                return ""

        # 如果值是空白字符串，则返回空字符串
        if value.strip() == "":
            print("TextbusField.get_prep_value: 值是空白字符串，返回空字符串")
            return ""

        print(f"TextbusField.get_prep_value: 返回处理后的值 = {repr(value)}")
        return value

    def to_python(self, value):
        """
        将数据库值转换为Python对象
        """
        # 打印调试信息
        print(f"TextbusField.to_python: 原始值 = {repr(value)}, 类型 = {type(value)}")

        # 如果值是None或空字符串或"None"或"undefined"，则返回空字符串
        if value is None or value == "" or value == "None" or value == "undefined":
            print("TextbusField.to_python: 返回空字符串")
            return ""

        # 确保值是字符串
        if not isinstance(value, str):
            try:
                value = str(value)
                print(f"TextbusField.to_python: 将非字符串值转换为字符串 = {repr(value)}")
            except Exception as e:
                print(f"TextbusField.to_python: 转换失败 = {e}")
                return ""

        # 如果值是空白字符串，则返回空字符串
        if value.strip() == "":
            print("TextbusField.to_python: 值是空白字符串，返回空字符串")
            return ""

        print(f"TextbusField.to_python: 返回处理后的值 = {repr(value)}")
        return value
