# -*- coding:utf-8 -*-
import os
from setuptools import find_packages, setup
from codecs import open

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-mdeditor-v3',
    version='0.2.2',
    packages=find_packages(exclude=['mdeditor_demo', 'mdeditor_demo_app.*', 'mdeditor_demo_app']),
    include_package_data=True,
    license='GPL-3.0 License',
    description='A simple Django app to edit markdown text with md-editor-v3.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mircool/django-mdeditor',
    author='mircool',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
