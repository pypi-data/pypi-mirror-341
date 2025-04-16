# This file is placed in the Public Domain.


"list of clients"


import threading


lock = threading.RLock()


class Fleet:

    "list of clients."

    clients = {}

    @staticmethod
    def add(clt) -> None:
        "add client to fleet."
        Fleet.clients[repr(clt)] = clt

    @staticmethod
    def all() -> []:
        "return all clients."
        yield from Fleet.clients.values()

    @staticmethod
    def announce(txt) -> None:
        "announce text on all clients."
        for clt in Fleet.clients.values():
            clt.announce(txt)

    @staticmethod
    def display(evt) -> None:
        "display result of an event."
        with lock:
            for tme in sorted(evt.result):
                Fleet.say(evt.orig, evt.channel, evt.result[tme])
            evt.ready()

    @staticmethod
    def first() -> None:
        "first clients in list."
        clt =  list(Fleet.clients.values())
        res = None
        if clt:
            res = clt[0]
        return res

    @staticmethod
    def get(orig) -> None:
        "client by origin."
        return Fleet.clients.get(orig, None)

    @staticmethod
    def say(orig, channel, txt) -> None:
        "echo text to channel."
        clt = Fleet.get(orig)
        if clt:
            clt.say(channel, txt)

    @staticmethod
    def wait() -> None:
        "wait for clients to shutdown."
        for clt in Fleet.clients.values():
            if "wait" in dir(clt):
                clt.wait()


def __dir__():
    return (
        'Fleet',
    )
