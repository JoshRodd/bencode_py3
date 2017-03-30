#bencode\_py3 1.1329139006

This package simply re-packages the existing bencoding and bdecoding
implemention from the "official" BitTorrent client as a separate,
leight-weight package for re-using them without having the entire
BitTorrent software as a dependency.

It is based on the implementation from BitTorrent Version 5.0.8. The
same calls are supported, but are implemented differently in order to
be compatible with Python 3.

Originally packaged by Tom Lazar, tom@tomster.org

It contains tests and a benchmark.

If you want to use this as a drop-in replacement for bencode, install
it, and then copy the ```bencode_py3``` directory in your
site-packages to ```bencode```, or else change your import statements.

Partially ported to work with Python 3 by Adam Delman.

Remainder ported to Python 3 and packaged by Josh Rodd, josh@rodd.us

Submit patches to http://github.com/JoshRodd/bencode_py3
