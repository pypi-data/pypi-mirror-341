import os
import re
from setuptools import setup, find_packages

# 从版本文件中读取版本号
with open(os.path.join('django_textbus', 'version.py'), 'r', encoding='utf-8') as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError('无法从版本文件中找到版本信息')

setup(
    name="django-textbus",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'django_textbus': [
            'templates/django_textbus/*.html',
            'static/django_textbus/js/*.js',
            'static/django_textbus/css/*.css',
        ],
    },
    license="MIT",
    description="A Django integration for Textbus rich text editor",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mircool/django-textbus",
    author="mircool",
    project_urls={
        "Bug Tracker": "https://github.com/mircool/django-textbus/issues",
        "Documentation": "https://github.com/mircool/django-textbus#readme",
        "Source Code": "https://github.com/mircool/django-textbus",
    },
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.0",
    ],
)
