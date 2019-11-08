# cython: infer_types=True
cimport cython
from libc.string cimport memcpy
from libcpp.set cimport set
from libc.stdint cimport uint32_t
from murmurhash.mrmr cimport hash64, hash32


cpdef hash_t hash_string(unicode string) except 0:
    chars = string.encode("utf8")
    return hash_utf8(chars, len(chars))


cdef hash_t hash_utf8(char* utf8_string, int length) nogil:
    return hash64(utf8_string, length, 1)


cdef unicode decode_Utf8Str(const Utf8Str* string):
    cdef int i, length
    if string.s[0] < sizeof(string.s) and string.s[0] != 0:
        return string.s[1:string.s[0]+1].decode("utf8")
    elif string.p[0] < 255:
        return string.p[1:string.p[0]+1].decode("utf8")
    else:
        i = 0
        length = 0
        while string.p[i] == 255:
            i += 1
            length += 255
        length += string.p[i]
        i += 1
        return string.p[i:length + i].decode("utf8")


cdef Utf8Str* _allocate(Pool mem, const unsigned char* chars, uint32_t length) except *:
    cdef int n_length_bytes
    cdef int i
    cdef Utf8Str* string = <Utf8Str*>mem.alloc(1, sizeof(Utf8Str))
    cdef uint32_t ulength = length
    if length < sizeof(string.s):
        string.s[0] = <unsigned char>length
        memcpy(&string.s[1], chars, length)
        return string
    elif length < 255:
        string.p = <unsigned char*>mem.alloc(length + 1, sizeof(unsigned char))
        string.p[0] = length
        memcpy(&string.p[1], chars, length)
        return string
    else:
        i = 0
        n_length_bytes = (length // 255) + 1
        string.p = <unsigned char*>mem.alloc(length + n_length_bytes, sizeof(unsigned char))
        for i in range(n_length_bytes-1):
            string.p[i] = 255
        string.p[n_length_bytes-1] = length % 255
        memcpy(&string.p[n_length_bytes], chars, length)
        return string


cdef class StringStore:
    """Look up strings by 64-bit hashes.

    DOCS: https://spacy.io/api/stringstore
    """
    def __init__(self):
        """Create the StringStore.

        strings (iterable): A sequence of unicode strings to add to the store.
        RETURNS (StringStore): The newly constructed object.
        """
        self.mem = Pool()
        self._map = PreshMap()

    def __getitem__(self, object string_or_id):
        """Retrieve a string from a given hash, or vice versa.

        string_or_id (bytes, unicode or uint64): The value to encode.
        Returns (unicode or uint64): The value to be retrieved.
        """
        if isinstance(string_or_id, basestring) and len(string_or_id) == 0:
            return 0
        elif string_or_id == 0:
            return ""
        cdef hash_t key
        if isinstance(string_or_id, unicode):
            key = hash_string(string_or_id)
            return key
        elif isinstance(string_or_id, bytes):
            key = hash_utf8(string_or_id, len(string_or_id))
            return key
        else:
            key = string_or_id
            utf8str = <Utf8Str*>self._map.get(key)
            if utf8str is NULL:
                raise KeyError()
            else:
                return decode_Utf8Str(utf8str)

    def as_int(self, key):
        """If key is an int, return it; otherwise, get the int value."""
        if not isinstance(key, basestring):
            return key
        else:
            return self[key]

    def as_string(self, key):
        """If key is a string, return it; otherwise, get the string value."""
        if isinstance(key, basestring):
            return key
        else:
            return self[key]
 
    def add(self, string):
        """Add a string to the StringStore.

        string (unicode): The string to add.
        RETURNS (uint64): The string's hash value.
        """
        if isinstance(string, unicode):
            key = hash_string(string)
            self.intern_unicode(string)
        elif isinstance(string, bytes):
            key = hash_utf8(string, len(string))
            self._intern_utf8(string, len(string))
        else:
            raise TypeError()
        return key

    def __len__(self):
        """The number of strings in the store.

        RETURNS (int): The number of strings in the store.
        """
        return self.keys.size()

    def __contains__(self, string not None):
        """Check whether a string is in the store.

        string (unicode): The string to check.
        RETURNS (bool): Whether the store contains the string.
        """
        cdef hash_t key
        if isinstance(string, int) or isinstance(string, long):
            if string == 0:
                return True
            key = string
        elif len(string) == 0:
            return True
        elif isinstance(string, unicode):
            key = hash_string(string)
        else:
            string = string.encode("utf8")
            key = hash_utf8(string, len(string))
        return self._map.get(key) is not NULL

    def __iter__(self):
        """Iterate over the strings in the store, in order.

        YIELDS (unicode): A string in the store.
        """
        cdef int i
        cdef hash_t key
        for i in range(self.keys.size()):
            key = self.keys[i]
            utf8str = <Utf8Str*>self._map.get(key)
            yield decode_Utf8Str(utf8str)
        # TODO: Iterate OOV here?

    def __reduce__(self):
        strings = list(self)
        return (StringStore, (strings,), None, None, None)

    def _reset_and_load(self, strings):
        self.mem = Pool()
        self._map = PreshMap()
        self.keys.clear()
        for string in strings:
            self.add(string)

    cdef const Utf8Str* intern_unicode(self, unicode py_string):
        # 0 means missing, but we don't bother offsetting the index.
        cdef bytes byte_string = py_string.encode("utf8")
        return self._intern_utf8(byte_string, len(byte_string))

    @cython.final
    cdef const Utf8Str* _intern_utf8(self, char* utf8_string, int length):
        # TODO: This function's API/behaviour is an unholy mess...
        # 0 means missing, but we don't bother offsetting the index.
        cdef hash_t key = hash_utf8(utf8_string, length)
        cdef Utf8Str* value = <Utf8Str*>self._map.get(key)
        if value is not NULL:
            return value
        value = _allocate(self.mem, <unsigned char*>utf8_string, length)
        self._map.set(key, value)
        self.keys.push_back(key)
        return value
