#!/usr/bin/env python3
from setuptools import setup

setup(
    name='kibana-backup-simple',
    version=open('VERSION', 'r').read().strip(),
    url='https://github.com/selivan/kibana-backup-simple',
    license='WTFPL',
    license_files = [ 'LICENSE' ],
    description='Simple backup/restore for Kibana saved objects: config, index patterns, dashboards, saved searches, etc.',
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',
    # twine requires author_email if author is set, but I don't like spam so homepage is enough
    author='Pavel Selivanov github.com/selivan',
    author_email='selivan.at.github@gmail-REMOVE-ANTI-SPAM.com',
    python_requires='>=3.5',
    install_requires=[
        'requests'
    ],
    scripts=['kibana-backup.py'],
    data_files=[('', ['LICENSE','VERSION','README.md'])],
)
