# coding=utf-8

TEMPLATE = u'''# Tox (https://tox.readthedocs.io/) is a tool for running tests
# in multiple virtualenvs. This configuration file will run the
# host_report suite on all supported python versions. To use it, "pip install tox"
# and then run "tox" from this directory.

[tox]
envlist = py27, py36

[testenv]
commands = python setup.py host_report
deps =
    pytest<4.1
    pytest-runner
    pytest-html
    pytest-cov
'''
