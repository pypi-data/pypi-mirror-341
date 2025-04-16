# This file is placed in the Public Domain.


"caching"


class Cache:

    """ object cache """

    objs = {}

    @staticmethod
    def add(path, obj) -> None:
        "add object to path entry"
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        "object at path"
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher) -> []:
        "match on key"
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)
