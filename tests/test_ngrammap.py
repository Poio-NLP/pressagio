import unittest

from pressagio.ngrammap import NgramMap


class TestNgramMap(unittest.TestCase):
    def setUp(self):
        self.ngram_map = NgramMap(2)

    def test_add(self):
        self.ngram_map.add(["hello", "world"])
        self.ngram_map.add(["hello", "new"])
        self.ngram_map.add(["hello", "new"])
        ngrams = list(self.ngram_map.items())
        self.assertEqual(len(ngrams), 2)
        self.assertEqual(ngrams[0][1], 1)
        self.assertEqual(ngrams[1][1], 2)

    def test_del(self):
        self.ngram_map.add(["hello", "world"])
        self.ngram_map.add(["hello", "new"])
        self.ngram_map.add(["hello", "new"])
        del self.ngram_map[["hello", "world"]]
        ngrams = list(self.ngram_map.items())
        self.assertEqual(len(ngrams), 1)
        self.assertEqual(ngrams[0][1], 2)
