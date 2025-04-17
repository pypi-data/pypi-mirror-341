"""
Django测试设置
"""

SECRET_KEY = 'django-insecure-test-key-only'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_textbus',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# 静态文件设置
STATIC_URL = '/static/'
STATICFILES_DIRS = []
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Textbus配置
TEXTBUS_CONFIG = {
    'height': '400px',
    'toolbar': ['bold', 'italic', 'underline'],
    'placeholder': '请输入内容...',
}
