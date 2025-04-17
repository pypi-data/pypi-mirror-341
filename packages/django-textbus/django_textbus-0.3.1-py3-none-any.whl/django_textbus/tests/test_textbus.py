from django.test import TestCase
from django import forms
from django.db import models

from django_textbus.widgets import TextbusWidget
from django_textbus.fields import TextbusField, TextbusFormField


class TextbusWidgetTest(TestCase):
    """测试TextbusWidget"""

    def test_widget_media(self):
        """测试小部件的媒体文件"""
        widget = TextbusWidget()
        # 检查媒体属性是否存在
        media = widget.media
        self.assertIsNotNone(media)
        # 现在我们直接从 CDN 加载文件，所以媒体对象应该是空的
        self.assertEqual(len(getattr(media, '_js', [])), 0)
        self.assertEqual(len(getattr(media, '_css', {}).get('all', [])), 0)

    def test_widget_attrs(self):
        """测试小部件的属性"""
        widget = TextbusWidget()
        self.assertEqual(widget.attrs['class'], 'textbus-editor')

        # 测试自定义属性
        widget = TextbusWidget(attrs={'rows': 10, 'class': 'custom-class'})
        self.assertEqual(widget.attrs['rows'], 10)
        self.assertEqual(widget.attrs['class'], 'custom-class')


class TextbusFieldTest(TestCase):
    """测试TextbusField"""

    def test_formfield(self):
        """测试字段的表单字段"""
        field = TextbusField()
        form_field = field.formfield()
        self.assertIsInstance(form_field, TextbusFormField)
        self.assertIsInstance(form_field.widget, TextbusWidget)

    def test_model_field(self):
        """测试模型字段"""
        # 创建一个测试模型
        class TestModel(models.Model):
            content = TextbusField()

            class Meta:
                app_label = 'test_app'

        # 检查字段类型
        field = TestModel._meta.get_field('content')
        self.assertIsInstance(field, TextbusField)
        self.assertEqual(field.description, "Textbus富文本字段")


class TextbusFormFieldTest(TestCase):
    """测试TextbusFormField"""

    def test_form_field(self):
        """测试表单字段"""
        field = TextbusFormField()
        self.assertIsInstance(field.widget, TextbusWidget)

        # 测试自定义配置
        config = {'height': '300px'}
        field = TextbusFormField(config=config)
        self.assertEqual(field.widget.config['height'], '300px')

        # 测试在表单中使用
        class TestForm(forms.Form):
            content = TextbusFormField()

        form = TestForm()
        self.assertIsInstance(form.fields['content'], TextbusFormField)
        self.assertIsInstance(form.fields['content'].widget, TextbusWidget)
