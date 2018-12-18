# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#

import distutils.core
try:
    import setuptools
except ImportError:
    pass

version = "0.2.11"

distutils.core.setup(
    name="nsqworker",
    version=version,
    packages=["nsqworker", "nsqworker.workers", "nsqworker.workers.demo"],
    author="Felinx Lee",
    author_email="felinx.lee@gmail.com",
    url="https://github.com/felinx/nsqworker",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="nsqworker is a skeletal code of one way to implement a nsq consumer in Python base on pynsq",
    install_requires=[
        "six",
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ]
)
