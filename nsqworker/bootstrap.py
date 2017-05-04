# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#

import logging
import nsq
from tornado import autoreload
from tornado.options import define, options

from nsqworker.workers.worker import load_worker

define("topic", default="demo", help="nsq topic")
define("topic_prefix", default="", help="nsq topic prefix")
define("channel", default="pageview", help="nsq topic channel")
define("nsq_max_processed_messages_queue", default=200,
       type=int, help="nsq max processed messages queue")
define("nsqlookupd_http_addresses", default="http://127.0.0.1:4161",
       multiple=True, help="nsqlookupd http addresses")
define("debug", default=False)


def run(workers_module="nsqworker.workers", **kw):
    worker = load_worker(workers_module)
    logging.debug("Starting worker: %s" % worker)
    topic = "%s%s" % (options.topic_prefix, options.topic)

    legacy = False
    try:
        from nsq import LegacyReader
    except ImportError:
        legacy = True

    if not legacy:
        # nsq 0.5+
        for name, handler in worker.handlers.iteritems():
            r = nsq.Reader(topic, "%s_%s" % (options.channel, name[0:-len("_handler")]),
                           message_handler=handler,
                           lookupd_http_addresses=options.nsqlookupd_http_addresses,
                           **kw)

            # override default preprocess and validate method with worker's
            # method
            r.validate_message = worker.validate_message
            r.preprocess_message = worker.preprocess_message
    else:
        # nsq 0.4
        r = nsq.Reader(all_tasks=worker.handlers,
                       topic=topic,
                       channel=options.channel,
                       lookupd_http_addresses=options.nsqlookupd_http_addresses,
                       **kw)

        r.validate_message = worker.validate_message
        r.preprocess_message = worker.preprocess_message

    if options.debug:
        autoreload.start()

    nsq.run()


if __name__ == "__main__":
    run()
