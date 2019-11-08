from libc.stdint cimport uint32_t, uint64_t
from libcpp.vector cimport vector
from libcpp.set cimport set

from cymem.cymem cimport Pool
from preshed.maps cimport PreshMap

from .strings cimport StringStore, hash_string, hash_utf8, decode_Utf8Str, Utf8Str


ctypedef uint64_t hash_t
ctypedef uint64_t attr_t


cdef struct Ngram:
    hash_t* value
    uint64_t count


cdef class NgramMap:
    cdef Pool mem
    cdef int ngram_size

    cdef public PreshMap _map
    cdef public StringStore _strings
