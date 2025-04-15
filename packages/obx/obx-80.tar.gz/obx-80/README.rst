OBX
===


**NAME**


``OBX`` - objects


**SYNOPSIS**


::

    >>> from obr import Object, dumps, loads
    >>> o = Object()
    >>> o.a = "b"
    >>> str(loads(dumps(o)))
    "{'a': 'b'}"


**DESCRIPTION**


``OBX`` allows for easy json save//load to/from disk of objects. It
provides an "clean namespace" Object class that only has dunder
methods, so the namespace is not cluttered with method names. This
makes storing and reading to/from json possible.


**INSTALL**


installation is done with pip

|
| ``$ pip install obx``
|


**AUTHOR**

|
| ``Bart Thate`` <``bthate@dds.nl``>
|

**COPYRIGHT**

|
| ``OBX`` is Public Domain.
|
