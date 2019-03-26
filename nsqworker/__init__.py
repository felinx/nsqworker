# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#
import functools

from nsqworker.initiator import Initiator
from nsqworker.workers.worker import Worker

__version__ = '0.2.11'

def channel(ch):
    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)

        inner._channel = ch
        return inner

    return outer
