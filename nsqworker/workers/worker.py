# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#

import time
import os
import sys
import traceback
import logging

from tornado import escape

from nsqworker.compat import import_module

_nsq_processed_messages_queues = {}

logger = logging.getLogger(__name__)


def load_worker(target_topic, target_channel, workers_module):
    """Load worker according to target_topic and target_channel.

     It only loads worker from file named as {topic}/{topic}_{channel}_worker.py,
     eg. demo/apiview_pageview_worker.py, the other files will be ignored.

    """
    # Preload all of workers
    mod = import_module(workers_module)
    workers_dir = os.path.dirname(os.path.abspath(mod.__file__))

    for d in os.listdir(workers_dir):
        dir_ = os.path.join(workers_dir, d)
        if os.path.isdir(dir_):
            topic = d
            channels = []
            for f in os.listdir(dir_):
                if not f.endswith("_worker.py"):
                    continue
                if not f.startswith('_') and f.endswith('.py'):
                    # topic_channel_worker
                    channels.append(f[len(topic) + 1:-len("_worker.py")])

            for channel in channels:
                try:
                    # preload
                    _load_worker(topic, channel, workers_module)
                except Exception as e:
                    logger.warning(e)
                    logger.warning(traceback.format_exc())

    try:
        worker, name = _load_worker(target_topic, target_channel,
                                    workers_module)
        if worker:
            return worker()
        else:
            raise ImportError("%s not found!" % name)
    except ImportError as e:
        logger.error(traceback.format_exc())
        raise e


class Worker(object):

    def preprocess_message(self, message):
        """JSON decode preprocess

        An optional callable that can alter the message data before other
        task functions are called.

        We assume that the message body is a JSON here.

        """
        try:
            message.body = escape.json_decode(escape.utf8(message.body))
        except ValueError:
            logger.error("Invalid JSON: %s", message.body)

        return message

    def validate_message(self, message):
        """An optional callable that returns a boolean as to weather or not
        this message should be processed.

        """
        if isinstance(message.body, dict):
            return True
        else:
            return False

    @property
    def handlers(self):
        _handlers = {}
        for func in dir(self):
            if func.endswith("_handler"):
                _handlers[func] = _handler(self, getattr(self, func), error_callback=self.handle_error)

        return _handlers

    def handle_error(self, exc_info=None):
        """
        Overried this method to perform error handling.
        """
        pass


def _handler(self, func, error_callback=None):
    """Worker handler decorator"""
    def wrapper(message):
        logger.debug("Raw message: %s, %s", message.id, message.body)
        try:
            now = time.time()
            r = func(message)
            logger.info(
                "Task elapse(%s-%s): %s", self.__class__.__name__,
                func.__name__, time.time() - now)
            if r is None:
                return True  # True by default
        except Exception as e:
            logger.debug(
                "Error message: %s, %s", message.id, message.body)
            exc_info = sys.exc_info()
            logger.error(e, exc_info=exc_info)
            if error_callback is not None:
                error_callback(exc_info=exc_info)

        return True

    return wrapper


def _load_worker(topic, channel, workers_module):
    mod_name = "%s_%s_worker" % (topic, channel)
    pkg = "%s.%s" % (workers_module, topic)
    mod = import_module(".%s" % mod_name, package=pkg)

    # topic_channel_worker to TopicChannelWorker
    name = "".join("%s%s" % (n[0].upper(), n[1:]) for n in mod_name.split("_"))
    worker = getattr(mod, name, None)

    return worker, name
