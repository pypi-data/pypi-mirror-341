# This file is placed in the Public Domain.


"read/write"


import datetime
import json
import os
import pathlib
import threading


from .json   import dump, load
from .object import update
from .path   import store


j = os.path.join
lock = threading.RLock()


class Error(Exception):

    """ disk error """


def cdir(pth) -> None:
    "create directory."
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def fqn(obj) -> str:
    "full qualifies name."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def getpath(obj):
    "return idented path."
    return j(store(ident(obj)))


def ident(obj) -> str:
    "mix full qualified name and a time stamp into a path."
    return j(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, pth) -> str:
    "read object from path."
    with lock:
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(pth) from ex
    return pth


def write(obj, pth=None) -> str:
    "write object to store, empty pth uses an idented path."
    with lock:
        if pth is None:
            pth = store(ident(obj))
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return pth


def __dir__():
    return (
        'cdir',
        'fqn',
        'getpath',
        'ident',
        'last',
        'long',
        'read',
        'search',
        'write'
    )
