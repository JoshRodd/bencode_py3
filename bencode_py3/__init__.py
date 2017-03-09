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
    elif x[f] == '0' and newf != f + 1:
        raise ValueError
    return (n, newf + 1)

def decode_string(bencoded_string, f):
    colon = bencoded_string.index(':', f)
    n = int(bencoded_string[f:colon])
    if bencoded_string[f] == '0' and colon != f + 1:
        raise ValueError
    colon += 1
    return (bencoded_string[colon:colon + n], colon + n)

def decode_list(bencoded_list, f):
    r, f = [], f + 1
    while bencoded_list[f] != 'e':
        v, f = decode_func[bencoded_list[f]](bencoded_list, f)
        r.append(v)
    return (r, f + 1)

def decode_dict(bencoded_dict, f):
    r, f = {}, f + 1
    while bencoded_dict[f] != 'e':
        k, f = decode_string(bencoded_dict, f)
        r[k], f = decode_func[bencoded_dict[f]](bencoded_dict, f)
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

def bdecode(bencoded_string):
    if isinstance(bencoded_string, bytes):
        bencoded_string = bencoded_string.decode("ascii")
    try:
        decoded_string, decoded_length = decode_func[bencoded_string[0]](bencoded_string, 0)
    except (IndexError, KeyError, ValueError):
        raise BTFailure("not a valid bencoded string")
    if decoded_length != len(bencoded_string):
        raise BTFailure("invalid bencoded value (data after valid prefix)")
    return decoded_string


class Bencached(object):

    __slots__ = ['bencoded']

    def __init__(self, s):
        self.bencoded = s

def encode_bencached(printable_obj):
    result_string = str()
    result_string += printable_obj.bencoded
    return result_string

def encode_int(int_obj):
    result_string = 'i'
    result_string += str(int_obj)
    result_string += 'e'
    return result_string

def encode_bool(bool_obj):
    result_string = ''
    if bool_obj: 
        result_string += encode_int(1)
    else:
        result_string += encode_int(0)
    return result_string
        
def encode_string(printable_string):
    result_string = str(len(printable_string))
    result_string += ':'
    result_string += printable_string
    return result_string

def encode_list(printable_obj_list):
    result_string = 'l'
    for i in printable_obj_list:
        result_string += encode_func[type(i)](i)
    result_string += 'e'
    return result_string

def encode_dict(printable_obj_dict):
    result_string = 'd'
    ilist = printable_obj_dict.items()
    ilist = sorted(ilist)
    for k, v in ilist:
        result_string += str(len(k))
        result_string += ':'
        result_string += k
        result_string += encode_func[type(v)](v)
    result_string += 'e'
    return result_string

encode_func = {}
encode_func[Bencached] = encode_bencached
encode_func[int] = encode_int
encode_func[str] = encode_string
encode_func[bytes] = encode_string
encode_func[list] = encode_list
encode_func[tuple] = encode_list
encode_func[dict] = encode_dict
encode_func[bool] = encode_bool

try:
    from types import BooleanType
    encode_func[BooleanType] = encode_bool
except ImportError:
    pass

def bencode(printable_obj):
    result_string = str()
    result_string += encode_func[type(printable_obj)](printable_obj)
    return result_string


