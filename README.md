#bencode_py3 1.101329139

This package simply re-packages the existing bencoding and bdecoding
implemention from the 'official' BitTorrent client as a separate,
leight-weight package for re-using them without having the entire
BitTorrent software as a dependency.

It currently uses the implementation from BitTorrent Version 5.0.8.
the file `bencode.py' is a verbatim, unmodified copy from that
distribution.

Originally packaged by Tom Lazar, tom@tomster.org

It does not contain any tests or a benchmark.

Ported to work with Python 3 by Adam Delman.

Packaged by Josh Rodd, josh@rodd.us
