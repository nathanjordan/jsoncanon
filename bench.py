import benchmark
import json
import jsoncanon


class CanonBench(benchmark.Benchmark):
    """ Benchmarks jsoncanon (with and without list sorting) against the json
        module for performance comparison """

    def setUp(self):
        self.size = 25000
        self.doc = {
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

    def test_jsoncanon(self):
        for i in xrange(self.size):
            jsoncanon.dumps(self.doc)

    def test_jsoncanon_sorting_lists(self):
        for i in xrange(self.size):
            jsoncanon.dumps(self.doc, sort_lists=True)

    def test_json_module(self):
        for i in xrange(self.size):
            json.dumps(self.doc)

if __name__ == "__main__":
    benchmark.main(format="rst")
