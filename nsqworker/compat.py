# -*- coding: utf-8 -*-

from importlib import import_module as _import

from six import PY3

def import_module(name, package=None):
	if PY3 and package is not None:
		_import(package)
	return _import(name, package=package)