# -*- coding: utf-8 -*-

import logging

import nsq
from nsqworker.workers.worker import load_worker
from six import iteritems
from tornado import autoreload

logger = logging.getLogger(__name__)


class Initiator(object):
    def __init__(self,
                 topic,
                 channel,
                 topic_prefix="",
                 nsq_max_processed_messages_queue=200,
                 nsqlookupd_http_addresses="http://127.0.0.1:4161"):
        self._topic = topic
        self._channel = channel
        self._topic_prefix = topic_prefix
        self._nsq_max_processed_messages_queue = nsq_max_processed_messages_queue
        self._nsqlookupd_http_addresses = nsqlookupd_http_addresses

    def run(self, workers_module="nsqworker.workers", debug=False, **kw):
        worker = load_worker(self._topic, self._channel, workers_module)
        logger.debug("Starting worker: %s" % worker)
        topic = "%s%s" % (self._topic_prefix, self._topic)

        legacy = False
        try:
            from nsq import LegacyReader
        except ImportError:
            legacy = True

        if not legacy:
            # nsq 0.5+
            for name, handler in iteritems(worker.handlers):
                r = nsq.Reader(
                    topic,
                    "%s_%s" % (self._channel, name[0:-len("_handler")]),
                    message_handler=handler,
                    lookupd_http_addresses=self._nsqlookupd_http_addresses,
                    **kw)

                # override default preprocess and validate method with worker's
                # method
                r.validate_message = worker.validate_message
                r.preprocess_message = worker.preprocess_message
        else:
            # nsq 0.4
            r = nsq.Reader(
                all_tasks=worker.handlers,
                topic=topic,
                channel=self._channel,
                lookupd_http_addresses=self._nsqlookupd_http_addresses,
                **kw)

            r.validate_message = worker.validate_message
            r.preprocess_message = worker.preprocess_message

        if debug:
            autoreload.start()

        nsq.run()
