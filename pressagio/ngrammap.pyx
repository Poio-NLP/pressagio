# cython: infer_types=True
cimport cython
from libc.string cimport memcpy
from libc.stdint cimport uint32_t

from murmurhash.mrmr cimport hash64


cdef class NgramMap:
    """
    Store and lookup ngrams by 64-bit hashes.
    """

    def __init__(self, ngram_size):
        self.mem = Pool()
        self.ngram_size = ngram_size
        self._map = PreshMap(initial_size=1000)
        self._strings = StringStore()

    def items(self):
        cdef size_t value
        cdef Ngram* ngram
        for value in self._map.values():
            ngram = <Ngram*>value
            ngram_strings = []
            for i in range(self.ngram_size):
                ngram_strings.append(self._strings[ngram.value[i]])
            yield ngram_strings, ngram.count

    def __len__(self):
        return len(self._map)

    def __delitem__(self, ngrams):
        cdef hash_t key = hash_string("\t".join(ngrams))
        del self._map[key]

    def add(self, ngrams):
        cdef hash_t key = hash_string("\t".join(ngrams))
        cdef Ngram* ngram
        cdef hash_t* new_ngram_keys
        ngram = <Ngram*>self._map.get(key)
        if ngram is not NULL:
            ngram.count += 1
        else:
            ngram = <Ngram*>self.mem.alloc(1, sizeof(Ngram))
            new_ngram_keys = <hash_t*>self.mem.alloc(self.ngram_size, sizeof(hash_t))
            for i in range(self.ngram_size):
                new_ngram_keys[i] = self._strings.add(ngrams[i])
            ngram.value = new_ngram_keys
            ngram.count = 1
            self._map.set(key, ngram)

