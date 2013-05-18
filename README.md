Overview
--------

nsqworker is a skeletal guide of one way to implement a [nsq][1] consumer in Python base on [pynsq][2], 
it is easy to implement a new consumer follow the conventions like ApiviewPageviewWorker in `workers/apiview/apiview_pageview_worker.py`

Conventions
-----------

1. Keep all of nsq workers of a topic in a sub-folder named the same as topic name, eg. nsqworker/workers/apiview/
2. Create a channel's worker in a file named `{topic}/{topic}_{channel}_worker.py`, eg. `workers/apiview/apiview_pageview_worker.py`
3. Implement the channel worker class, it should inherit from `nsqworker.workers.worker.Worker`, eg. ApiviewPageviewWorker(Worker)
4. Add a functional endswith `"_task"`(eg. `demo_task`) in the worker to handle messages, this functional will be treat as a task in pynsq automatically, you can add more than one task.

Demo
----

Run:

 	python main.py

and try to publish a message to topic apiview:

    curl -d '{"clicks": 10}' 'http://127.0.0.1:4151/put?topic=apiview'

then the worker will output:
	
    demo: apiview/pageview, clicks 10

If run main.py in command like below:

    python main.py --topic=newtopic --channel=newchannel

it will try to run NewtopicNewchannelWorker from `workers/newtopic/newtopic_newchannel_worker.py` which subscribes messages of newtopic/newchannel, of course, you need implement this worker.

  [1]: https://github.com/bitly/nsq
  [2]: https://github.com/bitly/pynsq
