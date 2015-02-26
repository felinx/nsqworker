# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#

import time
import os
import traceback
import logging
from tornado import escape
from tornado.options import options
from importlib import import_module

_nsq_processed_messages_queues = {}


def load_worker(workers_module):
    """Load worker according to topic and channel options.

     Preload all of workers to make tornado options work like a magic,
     so a worker can define custom options in worker's header.

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
                except Exception, e:
                    logging.warning(e)
                    logging.warning(traceback.format_exc())

    # Enable tornado command line options
    options.parse_command_line()

    # Then load the worker object according to topic and channel options.
    try:
        worker, name = _load_worker(options.topic, options.channel,
                                    workers_module)
        if worker:
            return worker()
        else:
            raise ImportError("%s not found!" % name)
    except ImportError, e:
        logging.error(traceback.format_exc())
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
            logging.error("Invalid JSON: %s", message.body)

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
                _handlers[func] = _handler(self, getattr(self, func))

        return _handlers


def _handler(self, func):
    """Worker handler decorator"""
    def wrapper(message):
        logging.debug("Raw message: %s, %s", message.id, message.body)
        try:
            now = time.time()
            r = func(message)
            logging.info(
                "Task elapse(%s-%s): %s", self.__class__.__name__,
                func.__name__, time.time() - now)
            if r is None:
                return True  # True by default
        except Exception, e:
            logging.debug(
                "Error message: %s, %s", message.id, message.body)
            logging.error(e)
            logging.error(traceback.format_exc())

        return True

    return wrapper


def _load_worker(topic, channel, workers_module):
    mod_name = "%s_%s_worker" % (topic, channel)
    mod = import_module(".%s" % mod_name,
                        package="%s.%s" % (workers_module, topic))

    # topic_channel_worker to TopicChannelWorker
    name = "".join("%s%s" % (n[0].upper(), n[1:]) for n in mod_name.split("_"))
    worker = getattr(mod, name, None)

    return worker, name
