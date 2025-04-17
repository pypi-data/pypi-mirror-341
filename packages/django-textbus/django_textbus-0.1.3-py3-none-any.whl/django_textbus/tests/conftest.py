"""
Pytest配置文件
"""
import os
import django

# 设置Django测试环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_textbus.tests.settings')
django.setup()
