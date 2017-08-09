# -*- coding: utf-8 -*-

from importlib import import_module as _import

from six import PY2

def import_module(name, package=None):
	if not PY2 and package is not None:
		_import(package)
	return _import(name, package=package)