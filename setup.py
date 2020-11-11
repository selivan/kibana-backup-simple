#!/usr/bin/env python3
from setuptools import setup

setup(
    name='kibana-backup-simple',
    version=open('VERSION', 'r').read(),
    url='https://github.com/selivan/kibana-backup-simple',
    license='WTFPL',
    description='Simple backup/restore for Kibana saved objects: config, index patterns, dashboards, saved searches, etc.',
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',
    author='Pavel Selivanov (selivan@github)',
    python_requires='>=3.5',
    install_requires=[
        'requests'
    ],
    scripts=['kibana-backup.py'],
)
