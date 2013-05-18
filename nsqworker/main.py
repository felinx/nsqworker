# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#

import logging
import sys
import nsq
from tornado.options import define, options

try:
    import nsqworker
except ImportError:
    import os
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from nsqworker.workers.worker import load_worker

define("topic", default="apiview", help="nsq topic")
define("channel", default="pageview", help="nsq topic channel")
define("nsq_max_processed_messages_queue", default=200, 
       type=int, help="nsq max processed messages queue")
define("nsqlookupd_http_addresses", default="http://127.0.0.1:4161", 
       multiple=True, help="nsqlookupd http addresses")


def main():
    worker = load_worker()
    logging.debug("Starting worker: %s" % worker)

    r = nsq.Reader(worker.tasks,
                   lookupd_http_addresses=options.nsqlookupd_http_addresses,
                   topic=options.topic, channel=options.channel)

    # override default preprocess and validate method with worker's method
    r.validate_message = worker.validate_message
    r.preprocess_message = worker.preprocess_message

    nsq.run()


if __name__ == "__main__":
    main()
