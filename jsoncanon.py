""" JSON canonicallizer module. It makes consistent representations of JSON
    objects for hashing and cryptography """
from __future__ import unicode_literals
from collections import OrderedDict


def dumps(element, sort_lists=False, excluded_keys=[], ignore_keyerror=False):
    """ Dumps a canonicallized string of a JSON compatible object. Excluded
        keys are removed from the top-level of a dictionary object (such as an
        id or metadata). Specifying sort_lists as True will sort all lists in
        the object. This is useful if the ordering of the list items is
        insignificant """
    # Excluded keys only work with dictionaries
    if type(element) is not dict and len(excluded_keys):
        raise ValueError("Cannot exclude keys for a non-dict type")
    # remove all the keys
    for key in excluded_keys:
        if not isinstance(key, str):
            raise ValueError("Excluded keys must be strings")
        try:
            del element[key]
        except KeyError:
            if not ignore_keyerror:
                raise ValueError("Excluded key does not exist in element")
    # canonicallize it!
    c = _Canonicallizer(sort_lists)
    return c.canon(element)


class _Canonicallizer(object):
    """ Funny name, serious results """

    def __init__(self, sort_lists):
        self.sort_lists = sort_lists

    def canon(self, e):
        """ Canonicallize the element to a uniform string """
        s = ""
        # return strings based on what type the object is
        if isinstance(e, dict):
            return self._wrap_dict(self._process_dict(s, e))
        elif isinstance(e, list):
            return self._wrap_list(self._process_list(s, e))
        elif isinstance(e, str):
            return self._wrap_string(e)
        elif isinstance(e, bool):
            return "true" if e is True else "false"
        elif isinstance(e, int):
            return str(e)
        elif isinstance(e, float):
            return str(e)
        elif isinstance(e, type(None)):
            return "null"
        # If its not a json type raise an error
        raise ValueError("Type %s cannot be serialized" % str(type(e)))

    def _wrap_list(self, s):
        """ Wraps the list in brackets """
        return "[" + s + "]"

    def _wrap_dict(self, s):
        """ wraps the dict in braces """
        return "{" + s + "}"

    def _wrap_string(self, s):
        """ wraps the string in quotes """
        return "\"" + s + "\""

    def _process_dict(self, s, d):
        """ Canonicallizes a dictionary by sorting the keys """
        # sort the dictionary keys
        od = OrderedDict(sorted(d.items()))
        # turn the dict into a string
        for i, k in enumerate(od):
            s += "\"" + k + "\":" + self.canon(od[k])
            if i < len(d.keys()) - 1:
                s += ","
        return s

    def _process_list(self, s, l):
        """ Canonicallizes a list """
        # if we're going to be sorting this list
        if self.sort_lists:
            # this is the ordering for the lists
            type_lists_dict = OrderedDict([
                ("dicts", []),
                ("lists", []),
                ("strings", []),
                ("ints", []),
                ("floats", []),
                ("bools", []),
                ("nulls", []),
            ])
            # separate the types into buckets
            self._categorize_list_items(type_lists_dict, l)
            # sort the buckets
            self._sort_type_lists(type_lists_dict)
            # create a list of the output strings (2nd element of the tuple)
            all_items = [i[1] for i in
                         self._concat_list_items(type_lists_dict)]
        # if we're not sorting this list
        else:
            # canon all the list items
            all_items = list(map(self.canon, l))
        # add these items (sorted or unsorted) to the canon string
        for i, item in enumerate(all_items):
            s += item
            if i < len(all_items) - 1:
                s += ","
        return s

    def _categorize_list_items(self, type_lists_dict, l):
        """ Separates items in the list by type (list, dict, string, etc.) """
        # check all the items in the list and put them in buckets
        for item in l:
            if isinstance(item, dict):
                x = self.canon(item)
                # the sort value for a dict is just its canonicallized string
                type_lists_dict['dicts'].append((x, x))
            elif isinstance(item, list):
                x = self.canon(item)
                # the sort value for a list is just its canonicallized string
                type_lists_dict['lists'].append((x, x))
            elif isinstance(item, str):
                # sort value for strings is the string itself
                type_lists_dict['strings'].append(
                    (item, self._wrap_string(item))
                )
            elif isinstance(item, int):
                # sort value for ints is itself
                type_lists_dict['ints'].append((item, str(item)))
            elif isinstance(item, float):
                # sort value for floats is itself
                type_lists_dict['floats'].append((item, str(item)))
            elif isinstance(item, bool):
                # sort value for bools is 0 for true and 1 for false
                x = (0, "true") if item else (1, "false")
                type_lists_dict['bools'].append(x)
            elif isinstance(item, type(None)):
                # sort value for null is 0
                type_lists_dict['nulls'].append((0, "null"))

    def _concat_list_items(self, type_lists_dict):
        """ Takes the separated types and puts them back together """
        concatenated_list = []
        # loop over the type lists in the type_lists dict
        for k, v in type_lists_dict.iteritems():
            # add them to the big list
            concatenated_list += v
        return concatenated_list

    def _sort_type_lists(self, type_lists_dict):
        """ Sort the type lists """
        # These are in a specific order by using OrderedDict
        for k, v in type_lists_dict.iteritems():
            # sort each type list
            type_lists_dict[k] = self._sort_type_list(v)

    def _sort_type_list(self, l):
        """ Sort a list of one type of list item """
        # Sort by the first element of the tuple
        return sorted(l, key=lambda x: x[0])
