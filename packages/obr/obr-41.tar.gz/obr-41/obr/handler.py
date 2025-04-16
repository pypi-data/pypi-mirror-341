# This file is placed in the Public Domain.


"handler"


import queue
import threading
import _thread


from .errors import later
from .thread import launch, name


lock = threading.RLock()


class Handler:

    """ callback handler """

    def __init__(self):
        self.cbs     = {}
        self.queue   = queue.Queue()
        self.ready   = threading.Event()
        self.stopped = threading.Event()

    def callback(self, evt) -> None:
        "call callback bacsed on events type."
        with lock:
            func = self.cbs.get(evt.type, None)
            if not func:
                evt.ready()
                return
            if evt.txt:
                cmd = evt.txt.split(maxsplit=1)[0]
            else:
                cmd = name(func)
            evt._thr = launch(func, evt, name=cmd) # pylint: disable=W0212

    def loop(self) -> None:
        "loop over events and call callback on them."
        while not self.stopped.is_set():
            evt = self.poll()
            if evt is None:
                break
            evt.orig = repr(self)
            try:
                self.callback(evt)
            except Exception as ex: # pylint: disable=W0718
                later(ex)
                _thread.interrupt_main()
        self.ready.set()

    def poll(self):
        "return event."
        return self.queue.get()

    def put(self, evt) -> None:
        "put event in queue/"
        self.queue.put(evt)

    def register(self, typ, cbs) -> None:
        "register callback."
        self.cbs[typ] = cbs

    def start(self) -> None:
        "start handler."
        self.stopped.clear()
        self.ready.clear()
        launch(self.loop)

    def stop(self) -> None:
        "stop handler."
        self.stopped.set()
        self.queue.put(None)

    def wait(self) -> None:
        "wait for handler to stop."
        self.ready.wait()


def __dir__():
    return (
        'Handler',
    )
