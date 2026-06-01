#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SyncPilot-CLI Setup Script
轻量级终端智能文件同步与备份引擎安装脚本
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='syncpilot-cli',
    version='1.0.0',
    description='Lightweight Terminal File Synchronization & Backup Engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SyncPilot Team',
    author_email='syncpilot@example.com',
    url='https://github.com/gitstq/SyncPilot-CLI',
    py_modules=['syncpilot'],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'syncpilot=syncpilot:main',
            'sp=syncpilot:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: Utilities',
    ],
    keywords='sync backup file-synchronization cli terminal tool',
    project_urls={
        'Bug Reports': 'https://github.com/gitstq/SyncPilot-CLI/issues',
        'Source': 'https://github.com/gitstq/SyncPilot-CLI',
    },
)
