# Django Textbus

Django Textbus 是一个 Django 应用，用于集成 [Textbus](https://textbus.io/) 富文本编辑器到 Django 项目中。

## 特性

- 为 Django 表单提供 Textbus 富文本编辑器小部件
- 支持 Django 4.0 及以上版本
- 可自定义的编辑器配置
- 简单易用的 API

## 安装

```bash
pip install django-textbus
```

## 快速开始

1. 将 `django_textbus` 添加到你的 `INSTALLED_APPS` 设置中：

```python
INSTALLED_APPS = [
    ...
    'django_textbus',
]
```

2. 在你的模型中使用 TextbusField：

```python
from django.db import models
from django_textbus.fields import TextbusField

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = TextbusField()
```

3. 在表单中使用 TextbusWidget：

```python
from django import forms
from django_textbus.widgets import TextbusWidget
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': TextbusWidget(),
        }
```

## 配置

你可以在 Django 的 settings.py 中配置 Textbus 编辑器：

```python
TEXTBUS_CONFIG = {
    'height': '400px',
    'toolbar': ['bold', 'italic', 'underline', 'strikethrough', 'link', 'image'],
    # 更多配置选项...
}
```

## 许可证

MIT
