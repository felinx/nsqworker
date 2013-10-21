Overview
--------

nsqworker is a skeletal code of one way to implement [nsq][1] consumer(worker) in Python base on [pynsq][2].


Installation
------------

    pip install nsqworker

Demo
----

Go to nsqworker root folder and run:

    python bootstrap.py

Publish a message to topic demo:

    curl -d '{"clicks": 10}' 'http://127.0.0.1:4151/put?topic=demo'

then the demo worker will output:

    demo: demo/pageview, clicks 10

If run bootstrap.py in command like below:

    python bootstrap.py --topic=newtopic --channel=newchannel

It will try to run NewtopicNewchannelWorker from `workers/newtopic/newtopic_newchannel_worker.py` which subscribes messages of newtopic/newchannel, of course, you need implement this worker.

Conventions
-----------

1. Keep all of nsq workers of a topic in a sub-folder named the same as the topic name, eg. nsqworker/workers/demo/
2. Create a channel's worker in a file named `{topic}/{topic}_{channel}_worker.py`, eg. `workers/demo/demo_pageview_worker.py`
3. Implement the channel worker class, it should inherit from `nsqworker.Worker`, eg. DemoPageviewWorker(Worker)
4. Add a functional endswith `"_handler"`(eg. `demo_handler`) in the worker to handle messages, this functional will be treated as a message_handler in pynsq automatically, you can add more than one handlers.

It is easy to implement a customize consumer follow this conventions.

Customize your bootstrap.py
---

    from nsqworker.bootstrap import run
    # Customize workers_module which default value is nsqworker.workers(The root module of demo workers)
    # You should set it to yourpackage.workers.
    run("yourpackage.workers")

Then it will load and run workers under yourpackage.workers like nsqworker.bootstrap.py


  [1]: https://github.com/bitly/nsq
  [2]: https://github.com/bitly/pynsq
