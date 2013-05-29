# -*- coding: utf-8 -*-
""" blc.py - a library written by John Smith to allow simple and pythonic
    interactions with the BlooCoin server via a platter of queries.

    Currently supports server protocol `1.2.0-stable` (commit: 4dc77c7a15)
"""

import socket
import json


class BLCException(Exception):
    """ The base of all Exceptions raised by blc.py
        Allows blanket exception catching (bad).
    """
    pass


class SocketException(BLCException):
    """ Something has gone wrong with creating, connecting
        or using our socket with the BLC server.
    """
    pass


class JSONParseException(BLCException):
    """ The data the BLC server returned wasn't able to be
        loaded by json.loads()
    """
    pass


class MiscException(BLCException):
    """ Something went wrong and we don't know what it was.
        This shouldn't happen, so you might want to freak out.
    """
    pass


class CommandFailure(BLCException):
    """ The server - for whatever reasons it has - failed execution
        of our given command.
    """
    pass


class MissingFields(BLCException):
    """ You left some fields out of a command, so we can't actually
        send the command off.
    """
    pass


class _Transaction(object):
    """ Lets us talk to the server
        Mostly for internal transparent use by the
        rest of the library.

        usage:
        >>> t = _Transaction("check_addr")
        >>> t({"addr": "foo"})

        If you want to monkeypatch the server for dev testing,
        you can set: blcpy._Transaction._server = (host, port)
    """
    _server = ("server.bloocoin.org", 3122)

    def __init__(self,
                 command,
                 timeout=2,
                 retries=0):
        self.command = command
        self._timeout = timeout
        # Not actually used. -- TODO
        self._retries = retries

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return

    def __call__(self, payload, _buffer=1024, _looping=False):
        data_in = dict(cmd=self.command, **payload)
        s = socket.socket()
        s.settimeout(self._timeout)
        try:
            s.connect(self._server)
            s.send(json.dumps(data_in))
            if _looping:
                data = ""
                while True:
                    rec = s.recv(_buffer)
                    if rec:
                        data += rec
                    else:
                        break
            else:
                data = s.recv(_buffer)
            s.close()
            data_out = json.loads(data)
            return data_out
        except socket.error as e:
            raise SocketException(e)
        except ValueError as e:
            raise JSONParseException(e)
        raise MiscException("Unable to parse and return data (??)")


class Query(object):
    """ Base class used by the various commands we query the
        server with.

        Used via lots of sneaky Python magic, namely **kwargs
        and overriding __call__, so the usage is simple:
        Note: command is hardcoded, so not required in init.
        >>> q = Query(foo="bar", baz=123)
        >>> q()

        If you want to monkeypatch the command for quick testing,
        you can either create a new Query() and set the command on
        that directly, or you can explicity set _cmd="foo" in your
        query constructor.
    """
    required = []
    command = "query"
    _looping = False

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if "_cmd" in kwargs:
            self.command = self.kwargs['_cmd']
        req = [r for r in self.required if r not in kwargs]
        if req:
            raise MissingFields("Missing: {0}".format(", ".join(req)))

    def __call__(self):
        t = _Transaction(self.command)
        d = t(self.kwargs, _looping=self._looping)
        if d['success'] is not True:
            raise CommandFailure("'{0}'".format(d['message']))
        return d['payload']


class Check(Query):
    """ Allows miners to verify whether or not a given POW is
        valid, and if so have it added to the given address'
        bean counter.
    """
    required = ['addr', 'winning_string', 'winning_hash']
    command = "check"


class CheckAddr(Query):
    """ Gives the bean counter (coin amount) for a given address.
    """
    required = ['addr']
    command = "check_addr"


class GetCoin(Query):
    """ Allows miners to get the current difficulty of the server.

        Named "get_coin" purely for backwards compatibility reasons.
    """
    command = "get_coin"


class MyCoins(Query):
    """ Similar to CheckAddr, but requires a valid password.
        Mainly used by wallets to verify account credentials.
    """
    required = ['addr', 'pwd']
    command = "my_coins"


class Register(Query):
    """ Allows registration of new addresses.

        The given address must be `len(addr) == 40`, or the server
        will reject it. There are currently no character set restrictions
        on the address or password, so anything works.
    """
    required = ['addr', 'pwd']
    command = "register"


class SendCoin(Query):
    """ Allows transactions via sending a given coin amount to another
        address. The given address must exist, or a CommandFailure will
        be raised.
    """
    required = ['addr', 'pwd', 'to', 'amount']
    command = "send_coin"


class TotalCoins(Query):
    """ Fetches the total amount of coins the server is aware of.
    """
    command = "total_coins"


class Transactions(Query):
    """ Lists all transactions to and from the given address.
        Requires the password attached to the address for some
        god-forsaken reason.
    """
    _looping = True
    required = ['addr', 'pwd']
    command = "transactions"
