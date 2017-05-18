#!/usr/bin/env python

from setuptools import setup

setup(
    name='device-info-service',
    version='0.1.0',
    author='Javier Cacheiro',
    author_email='bigdata-dev@cesga.es',
    url='https://github.com/javicacheiro/device-info-service',
    license='MIT',
    description='REST service for storing and retrieving device meta info',
    long_description=open('README.rst').read(),
    #py_modules=['consul'],
    install_requires=['Flask', 'kvstore', 'requests', 'gunicorn', 'coverage'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
