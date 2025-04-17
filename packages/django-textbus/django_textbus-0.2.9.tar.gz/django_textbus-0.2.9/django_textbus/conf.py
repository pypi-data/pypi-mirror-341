from django.conf import settings

# 默认Textbus配置
DEFAULT_CONFIG = {
    'height': '400px',
    'toolbar': [
        'bold', 'italic', 'underline', 'strikethrough',
        'heading', 'color', 'link', 'image', 'video',
        'orderedList', 'unorderedList', 'indent', 'outdent',
        'alignment', 'table', 'code', 'undo', 'redo'
    ],
    'placeholder': '请输入内容...',
}

# 获取用户配置，如果没有则使用默认配置
TEXTBUS_CONFIG = getattr(settings, 'TEXTBUS_CONFIG', DEFAULT_CONFIG)
