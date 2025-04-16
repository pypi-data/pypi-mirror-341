# This file is placed in the Public Domain.


"clients"


from .fleet   import Fleet
from .handler import Handler


class Client(Handler):

    """ fleet registered clients. """

    def __init__(self):
        Handler.__init__(self)
        Fleet.add(self)

    def announce(self, txt) -> None:
        "announce on all clients."

    def raw(self, txt) -> None:
        "output text."
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None: # pylint: disable=W0613
        "output text in chennel"
        self.raw(txt)


def __dir__():
    return (
        'Client',
    )
