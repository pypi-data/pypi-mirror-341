import os
import shutil
import tempfile
import urllib.request
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '下载并安装Textbus编辑器的静态文件'

    def add_arguments(self, parser):
        parser.add_argument(
            '--version',
            default='latest',
            help='要安装的Textbus版本（默认为最新版本）'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重新安装，即使文件已存在'
        )

    def handle(self, *args, **options):
        version = options['version']
        force = options['force']
        
        # 静态文件目录
        static_dir = Path(__file__).resolve().parent.parent.parent / 'static' / 'django_textbus'
        js_dir = static_dir / 'js'
        css_dir = static_dir / 'css'
        
        # 确保目录存在
        js_dir.mkdir(parents=True, exist_ok=True)
        css_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查文件是否已存在
        js_file = js_dir / 'textbus.js'
        css_file = css_dir / 'textbus.css'
        theme_file = css_dir / 'textbus-theme.css'
        
        if not force and js_file.exists() and css_file.exists() and theme_file.exists():
            self.stdout.write(self.style.SUCCESS('Textbus文件已存在，跳过安装。使用--force选项强制重新安装。'))
            return
        
        # 下载文件
        self.stdout.write('正在下载Textbus文件...')
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 下载JS文件
            if version == 'latest':
                js_url = 'https://unpkg.com/@textbus/editor/bundles/textbus.min.js'
                css_url = 'https://unpkg.com/@textbus/editor/bundles/textbus.min.css'
                theme_url = 'https://unpkg.com/@textbus/editor/bundles/textbus-theme.min.css'
            else:
                js_url = f'https://unpkg.com/@textbus/editor@{version}/bundles/textbus.min.js'
                css_url = f'https://unpkg.com/@textbus/editor@{version}/bundles/textbus.min.css'
                theme_url = f'https://unpkg.com/@textbus/editor@{version}/bundles/textbus-theme.min.css'
            
            # 下载文件
            try:
                temp_js = os.path.join(temp_dir, 'textbus.js')
                temp_css = os.path.join(temp_dir, 'textbus.css')
                temp_theme = os.path.join(temp_dir, 'textbus-theme.css')
                
                urllib.request.urlretrieve(js_url, temp_js)
                urllib.request.urlretrieve(css_url, temp_css)
                urllib.request.urlretrieve(theme_url, temp_theme)
                
                # 复制文件到静态目录
                shutil.copy2(temp_js, js_file)
                shutil.copy2(temp_css, css_file)
                shutil.copy2(temp_theme, theme_file)
                
                self.stdout.write(self.style.SUCCESS('Textbus文件安装成功！'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'下载Textbus文件时出错: {e}'))
                return
        
        # 提醒用户运行collectstatic
        self.stdout.write(self.style.WARNING('请记得运行 "python manage.py collectstatic" 以收集静态文件。'))
