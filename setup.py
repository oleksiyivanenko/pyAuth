# -*- coding: utf-8 -*-

__author__ = 'Alex Ivanenko'

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
	options = {'py2exe': {'bundle_files': 3, 'compressed': True}},
	windows = [{'script': "pyAuth.py"}],
	zipfile = None,
	)