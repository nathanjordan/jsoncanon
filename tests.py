""" Tests for jsoncanon """
from unittest import TestCase
import jsoncanon


def remove_endline(s):
    """ Removes carriage returns from strings read from files """
    return s[0:len(s) - 1]


class JsonCanonTest(TestCase):

    def test_all(self):
        truth = remove_endline(open("json/testall.json").read())
        d = {
            "a": [
                10,
                {},
                {
                    "hello": 1,
                    "zzz": []
                },
                "bob",
                "agnes"
            ],
            "1": 55.7,
            "3": {
                "xxxxx": {},
                "ggg": []
            },
            "b": None,
            "c": True,
            "d": False
        }
        s = jsoncanon.dumps(d)
        self.assertEqual(s, truth)
