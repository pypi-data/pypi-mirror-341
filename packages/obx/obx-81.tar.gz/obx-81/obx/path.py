# This file is placed in the Public Domain.


"paths with working directory"


import os
import pathlib


j = os.path.join


class Workdir: # pylint: disable=R0903

    """ path to objects """

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr  = ""


def long(name) -> str:
    "name to long name"
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir():
    "modules directory"
    return j(Workdir.wdr, "mods")


def pidname(name) -> str:
    "path to pid file"
    return j(Workdir.wdr, f"{name}.pid")


def skel() -> str:
    "basic directories"
    path = pathlib.Path(store())
    path.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(moddir())
    path.mkdir(parents=True, exist_ok=True)
    return path


def setwd(path):
    "set working directory"
    Workdir.wdr = path


def store(pth="") -> str:
    "path to store"
    return j(Workdir.wdr, "store", pth)


def strip(pth, nmr=2) -> str:
    "strip directory"
    return os.sep.join(pth.split(os.sep)[-nmr:])


def types() -> [str]:
    "return available types"
    return os.listdir(store())


def wdr(pth):
    "set working directory"
    return j(Workdir.wdr, pth)


def __dir__():
    return (
        'Workdir',
        'long',
        'moddir',
        'pidname',
        'skel',
        'store',
        'types',
        'wdr'
    )
