#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from os import environ as env
import subprocess

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

requirements = [str(req.requirement) for req in parse_requirements('requirements.txt', session=False)]
requirements_plugins = [str(req.requirement) for req in parse_requirements('requirements-plugins.txt', session=False)]

all_requirements = list()
for i in requirements + requirements_plugins:
    if i.startswith("git+"):
        all_requirements.append(i.split("#egg=")[-1:][0])
    else:
        all_requirements.append(i)

try:
    VERSION = subprocess.check_output(['git', 'describe', '--tags']).strip()
except subprocess.CalledProcessError:
    VERSION = '0.dev'

setup(
    name='cabot',
    version=VERSION,
    description="Self-hosted, easily-deployable monitoring and alerts service"
                " - like a lightweight PagerDuty",
    long_description=open('README.md').read(),
    author="Arachnys",
    author_email='info@arachnys.com',
    url='http://cabotapp.com',
    license='MIT',
    install_requires=all_requirements,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cabot = cabot.entrypoint:main',
        ],
    },
    zip_safe=False
)
