# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by Petru Paler
# Partially ported to Python 3 by Adam Delman
# Remainder ported to Python 3 by Josh Rodd

class BTFailure(Exception):
    pass

def decode_int(x, f):
    f += 1
    newf = x.index('e', f)
    n = int(x[f:newf])
    if x[f] == '-':
        if x[f + 1] == '0':
            raise ValueError
    elif x[f] == '0' and newf != f+1:
        raise ValueError
    return (n, newf+1)

def decode_string(x, f):
    colon = x.index(':', f)
    n = int(x[f:colon])
    if x[f] == '0' and colon != f+1:
        raise ValueError
    colon += 1
    return (x[colon:colon+n], colon+n)

def decode_list(x, f):
    r, f = [], f+1
    while x[f] != 'e':
        v, f = decode_func[x[f]](x, f)
        r.append(v)
    return (r, f + 1)

def decode_dict(x, f):
    r, f = {}, f+1
    while x[f] != 'e':
        k, f = decode_string(x, f)
        r[k], f = decode_func[x[f]](x, f)
    return (r, f + 1)

decode_func = {
    'l': decode_list,
    'd': decode_dict,
    'i': decode_int,
}
for x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
    decode_func[x] = decode_string

def bdecode(x):
    return bdecode_ascii(x if not isinstance(x, bytes) else x.decode("ascii"))

def bdecode_ascii(x):
    try:
        r, l = decode_func[x[0]](x, 0)
    except (IndexError, KeyError, ValueError):
        raise BTFailure("not a valid bencoded string")
    if l != len(x):
        raise BTFailure("invalid bencoded value (data after valid prefix)")
    return r

encode_func3 = {
    int: lambda x: ''.join(('i', str(x), 'e')),
    bool: lambda x: bencode3(1) if x else bencode3(0),
    bytes: lambda x: ''.join((str(len(x.decode('ascii'))), ':', x.decode('ascii'))),
    str: lambda x: ''.join((str(len(x)), ':', x)),
    list:  lambda x:\
       ''.join(('l', ''.join([bencode3(i) for i in x]), 'e')),
    dict: lambda x:\
       ''.join(('d', ''.join([(''.join((bencode3(k), bencode3(v))))\
       for k, v in sorted(x.items())]), 'e')),
}

bencode3 = lambda x: encode_func3[type(x)](x)

encode_func3[tuple] = encode_func3[list]

# For backwards compatibility only
class Bencached(object):
    __slots__ = ['bencoded']
    def __init__(self, s):
        self.bencoded = s

def encode_bencached(x, r):
    r.append(x.bencoded)

encode_func3[Bencached] = lambda x: x.bencoded

def encode_int(x, r):
    r.extend(('i', str(x), 'e'))

def encode_bool(x, r):
    encode_int(1, r) if x else encode_int(0, r)

def encode_string(x, r):
    r.extend((str(len(x)), ':', x))

def encode_bytes(x, r):
    encode_string(x.decode('ascii'), r)

def encode_list(x, r):
    r.append('l')
    for i in x:
        encode_func[type(i)](i, r)
    r.append('e')

def encode_dict(x,r):
    r.append('d')
    for k, v in sorted(x.items()):
        r.extend((str(len(k)), ':', k))
        encode_func[type(v)](v, r)
    r.append('e')

encode_func = {
    Bencached: encode_bencached,
    int: encode_int,
    bool: encode_bool,
    str: encode_string,
    list: encode_list,
    dict: encode_dict,
#    bytes: encode_bytes,
}

encode_func[tuple] = encode_func[list]

# For Python 3.x
try:
    encode_func[bytes] = encode_bytes
except NameError:
    pass

# For Python 2.x
try:
    encode_func3[unicode] = encode_func3[str]
    encode_func[unicode] = encode_func[str]
except NameError:
    pass

try:
    from types import BooleanType
    encode_func3[BooleanType] = encode_func3[bool]
    encode_func[BooleanType] = encode_func[bool]
except ImportError:
    pass

try:
    from types import StringType
    encode_func3[StringType] = encode_func3[str]
    encode_func[StringType] = encode_func[str]
except ImportError:
    pass

try:
    from types import IntType
    encode_func3[IntType] = encode_func3[int]
    encode_func[IntType] = encode_func[int]
except ImportError:
    pass

try:
    from types import LongType
    encode_func3[LongType] = encode_func3[int]
    encode_func[LongType] = encode_func[int]
except ImportError:
    pass

try:
    from types import DictType
    encode_func3[DictType] = encode_func3[dict]
    encode_func[DictType] = encode_func[dict]
except ImportError:
    pass

try:
    from types import TupleType
    encode_func3[TupleType] = encode_func3[tuple]
    encode_func[TupleType] = encode_func[tuple]
except ImportError:
    pass

def bencode2(x):
    r = []
    encode_func[type(x)](x, r)
    return ''.join(r)

bencode = bencode3
