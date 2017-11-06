# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#

from tornado.options import define, options

from nsqworker.initiator import Initiator

define("topic", default="demo", help="nsq topic")
define("topic_prefix", default="", help="nsq topic prefix")
define("channel", default="pageview", help="nsq topic channel")
define(
    "nsq_max_processed_messages_queue",
    default=200,
    type=int,
    help="nsq max processed messages queue")
define(
    "nsqlookupd_http_addresses",
    default="http://127.0.0.1:4161",
    multiple=True,
    help="nsqlookupd http addresses")
define("debug", default=False)


def run(workers_module="nsqworker.workers", **kw):
    initiator = Initiator(
        options.topic,
        options.channel,
        topic_prefix=options.topic_prefix,
        nsq_max_processed_messages_queue=options.
        nsq_max_processed_messages_queue,
        nsqlookupd_http_addresses=options.nsqlookupd_http_addresses)
    initiator.run(workers_module=workers_module, debug=options.debug, **kw)


if __name__ == "__main__":
    run()