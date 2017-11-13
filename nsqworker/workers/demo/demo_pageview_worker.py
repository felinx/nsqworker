# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#

import logging
from tornado.options import options, define
from nsqworker import Worker

define("demoname", "demo")

logger = logging.getLogger(__name__)


class DemoPageviewWorker(Worker):
    def demo_handler(self, message):
        logger.info("%s: %s/%s, clicks %s", options.demoname,
                     options.topic, options.channel, message.body.get("clicks", 1))

        return True
