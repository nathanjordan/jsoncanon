from collections import OrderedDict
from types import NoneType


def dumps(element, sort_lists=False, excluded_keys=[], ignore_keyerror=False):
    if type(element) is not dict and len(excluded_keys):
        raise ValueError("Cannot exclude keys for a non-dict type")
    for key in excluded_keys:
        if type(key) not in [unicode, str]:
            raise ValueError("""Excluded keys must be strings or unicode
                             objects""")
        try:
            del element[key]
        except KeyError:
            if not ignore_keyerror:
                raise ValueError("Excluded key does not exist in element")
    return _canon(element)

def _canon(e):
    """ Canonicallize the dictionary to a uniform string """
    s = ""
    if type(e) is list:
        return _wrap_list(_process_list(s, e))
    elif type(e) is dict:
        return _wrap_dict(_process_dict(s, e))
    elif type(e) in [unicode, str]:
        return "\"" + e + "\""
    elif type(e) is bool:
        return "true" if e is True else "false"
    elif type(e) is int:
        return str(e)
    elif type(e) is float:
        return str(e)
    elif type(e) is NoneType:
        return "null"
    raise ValueError("Type %s cannot be serialized" % str(type(e)))


def _wrap_list(s):
    return "[" + s + "]"


def _wrap_dict(s):
    return "{" + s + "}"


def _wrap_string(s):
    return "\"" + s + "\""


def _process_dict(s, d):
    od = OrderedDict(sorted(d.items()))
    for i, k in enumerate(od):
        s += "\"" + k + "\":" + canon(od[k])
        if i < len(d.keys()) - 1:
            s += ","
    return s


def _process_list(s, l):
    type_lists_dict = OrderedDict([
        ("dicts", []),
        ("lists", []),
        ("strings", []),
        ("ints", []),
        ("floats", []),
        ("bools", []),
        ("nulls", []),
    ])
    _process_list_types(type_lists_dict, l)
    _sort_type_lists(type_lists_dict)
    all_items = _concat_type_lists(type_lists_dict)
    for i, item in enumerate(all_items):
        s += item[1]
        if i < len(all_items) - 1:
            s += ","
    return s


def _process_list_types(type_lists_dict, l):
    for item in l:
        if type(item) is dict:
            x = canon(item)
            type_lists_dict['dicts'].append((x, x))
        elif type(item) is list:
            x = canon(item)
            type_lists_dict['lists'].append((x, x))
        elif type(item) in [unicode, str]:
            x = unicode(item)
            type_lists_dict['strings'].append((x, _wrap_string(x)))
        elif type(item) is int:
            type_lists_dict['ints'].append((item, str(item)))
        elif type(item) is float:
            type_lists_dict['floats'].append((item, str(item)))
        elif type(item) is bool:
            x = (0, "true") if item else (1, "false")
            type_lists_dict['bools'].append(x)
        elif type(item) is NoneType:
            type_lists_dict['nulls'].append((0, "null"))


def _concat_type_lists(type_lists_dict):
    concatenated_list = []
    for k, v in type_lists_dict.iteritems():
        concatenated_list += v
    return concatenated_list


def _sort_type_lists(type_lists_dict):
    for k, v in type_lists_dict.iteritems():
        type_lists_dict[k] = _sort_type_list(v)


def _sort_type_list(l):
    return sorted(l, key=lambda x: x[0])
