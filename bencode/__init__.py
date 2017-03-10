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

decode_func = {}
decode_func['l'] = decode_list
decode_func['d'] = decode_dict
decode_func['i'] = decode_int
decode_func['0'] = decode_string
decode_func['1'] = decode_string
decode_func['2'] = decode_string
decode_func['3'] = decode_string
decode_func['4'] = decode_string
decode_func['5'] = decode_string
decode_func['6'] = decode_string
decode_func['7'] = decode_string
decode_func['8'] = decode_string
decode_func['9'] = decode_string

def bdecode(x):
    if isinstance(x, bytes):
        x = x.decode("ascii")
    try:
        r, l = decode_func[x[0]](x, 0)
    except (IndexError, KeyError, ValueError):
        raise BTFailure("not a valid bencoded string")
    if l != len(x):
        raise BTFailure("invalid bencoded value (data after valid prefix)")
    return r


encode_func = {}

bencode = lambda x: encode_func[type(x)](x)

encode_func[int] = lambda x: ''.join(('i', str(x), 'e'))
encode_func[bool] = lambda x: bencode(1) if x else bencode(0)
encode_func[str] = lambda x: ''.join((str(len(x)), ':', x))
encode_func[bytes] = encode_func[str]
encode_func[list] = lambda x: ''.join(('l', ''.join([bencode(i) for i in x]), 'e'))
encode_func[tuple] = encode_func[list]
encode_func[dict] = lambda x: ''.join(('d', ''.join([(''.join((bencode(k), bencode(v)))) for k, v in sorted(x.items())]), 'e'))

# For Python 2.x
try:
    encode_func[unicode] = encode_func[str]
except NameError:
    pass

try:
    from types import BooleanType
    encode_func[BooleanType] = encode_func[bool]
except ImportError:
    pass

try:
    from types import StringType
    encode_func[StringType] = encode_func[str]
except ImportError:
    pass

try:
    from types import IntType
    encode_func[IntType] = encode_func[int]
except ImportError:
    pass

try:
    from types import LongType
    encode_func[LongType] = encode_func[int]
except ImportError:
    pass

try:
    from types import DictType
    encode_func[DictType] = encode_func[dict]
except ImportError:
    pass

try:
    from types import TupleType
    encode_func[TupleType] = encode_func[tuple]
except ImportError:
    pass
