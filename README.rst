jsoncanon
=================
.. image:: https://travis-ci.org/nathanjordan/jsoncanon.svg
    :target: https://travis-ci.org/nathanjordan/jsoncanon

.. image:: https://coveralls.io/repos/nathanjordan/jsoncanon/badge.png?branch=master
  :target: https://coveralls.io/r/nathanjordan/jsoncanon?branch=master

A Python library that creates a canonicalized version of a JSON document for
uniqueness checking, hashing, and cryptography

Benchmark Report
------------------------------

CanonBench
----------

+-------------------------+------+------+--------+---------+---------------+
|                    name | rank | runs |   mean |      sd | timesBaseline |
+=========================+======+======+========+=========+===============+
|             json module |    1 |    5 | 0.2205 | 0.06855 |           1.0 |
+-------------------------+------+------+--------+---------+---------------+
|               jsoncanon |    2 |    5 |  2.571 |  0.1222 | 11.6598209591 |
+-------------------------+------+------+--------+---------+---------------+
| jsoncanon sorting lists |    3 |    5 |  6.916 |   2.016 | 31.3608244859 |
+-------------------------+------+------+--------+---------+---------------+

Each of the above 15 runs were run in random, non-consecutive order by
`benchmark` v0.1.5 (http://jspi.es/benchmark) with Python 2.7.6
Darwin-13.1.0-x86_64 on 2014-05-18 21:53:23
