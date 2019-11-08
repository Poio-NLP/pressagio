"""
Several classes to tokenize text.

"""
import abc
import codecs
import collections
import re
import bisect

import pressagio.character


class Tokenizer(object):
    """
    Base class for all tokenizers.

    """

    __metaclass__ = abc.ABCMeta

    def __init__(
        self,
        text,
        blankspaces=pressagio.character.blankspaces,
        separators=pressagio.character.separators,
    ):
        """
        Constructor of the Tokenizer base class.

        Parameters
        ----------
        text : str
            The text to tokenize.

        blankspaces : str
            The characters that represent empty spaces.

        separators : str
            The characters that separate token units (e.g. word boundaries).

        """
        self.separators = separators
        self.blankspaces = blankspaces
        self.text = text
        self.lowercase = False

        self.offbeg = 0
        self.offset = None
        self.offend = None

    def is_blankspace(self, char):
        """
        Test if a character is a blankspace.

        Parameters
        ----------
        char : str
            The character to test.

        Returns
        -------
        ret : bool
            True if character is a blankspace, False otherwise.

        """
        if len(char) > 1:
            raise TypeError("Expected a char.")
        if char in self.blankspaces:
            return True
        return False

    def is_separator(self, char):
        """
        Test if a character is a separator.

        Parameters
        ----------
        char : str
            The character to test.

        Returns
        -------
        ret : bool
            True if character is a separator, False otherwise.

        """
        if len(char) > 1:
            raise TypeError("Expected a char.")
        if char in self.separators:
            return True
        return False

    @abc.abstractmethod
    def count_characters(self):
        raise NotImplementedError("Method must be implemented")

    @abc.abstractmethod
    def reset_stream(self):
        raise NotImplementedError("Method must be implemented")

    @abc.abstractmethod
    def count_tokens(self):
        raise NotImplementedError("Method must be implemented")

    @abc.abstractmethod
    def has_more_tokens(self):
        raise NotImplementedError("Method must be implemented")

    @abc.abstractmethod
    def next_token(self):
        raise NotImplementedError("Method must be implemented")

    @abc.abstractmethod
    def progress(self):
        raise NotImplementedError("Method must be implemented")


class ForwardTokenizer(Tokenizer):
    def __init__(
        self,
        text,
        blankspaces=pressagio.character.blankspaces,
        separators=pressagio.character.separators,
    ):
        Tokenizer.__init__(self, text, blankspaces, separators)

        self.offend = self.count_characters() - 1
        self.reset_stream()

    def count_tokens(self):
        count = 0
        while self.has_more_tokens():
            count += 1
            self.next_token()

        self.reset_stream()

        return count

    def count_characters(self):
        """
        Counts the number of unicode characters in the IO stream.

        """
        return len(self.text)

    def has_more_tokens(self):
        if self.offset < self.offend:
            return True
        return False

    def next_token(self):
        current = self.text[self.offset]
        self.offset += 1
        token = ""

        if self.offset <= self.offend:
            while (
                self.is_blankspace(current) or self.is_separator(current)
            ) and self.offset < self.offend:
                current = self.text[self.offset]
                self.offset += 1

            while (
                not self.is_blankspace(current)
                and not self.is_separator(current)
                and self.offset <= self.offend
            ):

                if self.lowercase:
                    current = current.lower()

                token += current

                current = self.text[self.offset]
                self.offset += 1

                if self.offset > self.offend:
                    token += self.text[-1]

        return token

    def progress(self):
        return float(offset) / offend

    def reset_stream(self):
        self.offset = 0


class ReverseTokenizer(Tokenizer):
    def __init__(
        self,
        text,
        blankspaces=pressagio.character.blankspaces,
        separators=pressagio.character.separators,
    ):
        Tokenizer.__init__(self, text, blankspaces, separators)

        self.offend = self.count_characters() - 1
        self.offset = self.offend

    def count_tokens(self):
        curroff = self.offset
        self.offset = self.offend
        count = 0
        while self.has_more_tokens():
            self.next_token()
            count += 1
        self.offset = curroff
        return count

    def count_characters(self):
        """
        Counts the number of unicode characters in the IO stream.

        """
        return len(self.text)

    def has_more_tokens(self):
        if self.offbeg <= self.offset:
            return True
        else:
            return False

    def next_token(self):
        token = ""

        while (self.offbeg <= self.offset) and len(token) == 0:
            current = self.text[self.offset]

            if (self.offset == self.offend) and (
                self.is_separator(current) or self.is_blankspace(current)
            ):
                self.offset -= 1
                return token

            while (
                self.is_blankspace(current) or self.is_separator(current)
            ) and self.offbeg < self.offset:
                self.offset -= 1
                if self.offbeg <= self.offset:
                    current = self.text[self.offset]

            while (
                not self.is_blankspace(current)
                and not self.is_separator(current)
                and self.offbeg <= self.offset
            ):
                if self.lowercase:
                    current = current.lower()
                token = current + token
                self.offset -= 1
                if self.offbeg <= self.offset:
                    current = self.text[self.offset]

        return token

    def progress(self):
        return float(self.offend - self.offset) / (self.offend - self.offbeg)

    def reset_stream(self):
        self.offset = self.offend


def preprocess(text):
    re_wordbeg = re.compile(r"(?<=\s)[-']")
    re_wordbeg2 = re.compile(r"(?<=\s\")[-']")
    re_wordend = re.compile(r"[-'](?=\s)")
    re_wordend2 = re.compile(r"[-'](?=\"\s)")
    text = re_wordbeg.sub("", text)
    text = re_wordbeg2.sub("", text)
    text = re_wordend.sub("", text)
    text = re_wordend2.sub("", text)
    return text


class NgramMap:
    """
    A memory efficient store for ngrams.

    This class is optimized for memory consumption, it might be slower than
    other ngram stores. It is also optimized for a three step process:

    1) Add all ngrams.
    2) Perform a cutoff opertation (optional).
    3) Read list of ngrams.

    It might not perform well for other use cases.
    """

    def __init__(self):
        """Initialize internal data stores."""
        self._strings = dict()
        self.ngrams = collections.defaultdict(int)
        self.next_index = 0

    def add_token(self, token):
        """
        Add a token to the internal string store.

        This will only add the token to the internal strings store. It will
        return an index that you can use to create your ngram.

        The ngrams a are represented as strings of the indices, so we will
        return a string here so that the consumer does not have to do the
        conversion.

        Parameters
        ----------
        token : str
            The token to add to the string store.

        Returns
        -------
        str
            The index of the token as a string.
        """
        if token in self._strings:
            return str(self._strings[token])
        else:
            self._strings[token] = self.next_index
            old_index = self.next_index
            self.next_index += 1
            return str(old_index)

    def add(self, ngram_indices):
        """
        Add an ngram to the store.

        This will add a list of strings as an ngram to the ngram store. In our
        standard use case the strings are the indices of the strings, you can
        get those from the `add_token()` method.

        Parameters
        ----------
        list of str
            The indices of the ngram strings as string.
        """
        self.ngrams["\t".join(ngram_indices)] += 1

    def cutoff(self, cutoff):
        """
        Perform a cutoff on the ngram store.

        This will remove all ngrams that have a frequency with the given cutoff
        or lower.

        Parameters
        ----------
        cutoff : int
            The cutoff value, we will remove all items with a frequency of the
            cutoff or lower.
        """
        delete_keys = []
        for k, count in self.ngrams.items():
            if count <= cutoff:
                delete_keys.append(k)
        for k in delete_keys:
            del self.ngrams[k]

    def __len__(self):
        """Return the number of ngrams in the store."""
        return len(self.ngrams)

    def items(self):
        """
        Get the ngrams from the store.

        Returns
        -------
        iterable of tokens, count
            The tokens are a list of strings, the real tokens that you added
            to the store via `add_token()`. The count is the the count value
            for that ngram.
        """
        strings = {v: k for k, v in self._strings.items()}
        for token_indices, count in self.ngrams.items():
            tokens = [strings[int(idx)] for idx in token_indices.split("\t")]
            yield tokens, count


def forward_tokenize_file(infile, ngram_size, lowercase=False, cutoff=0):
    """
    Tokenize a file and return an ngram store.

    Parameters
    ----------
    infile : str
        The file to parse.
    ngram_size : int
        The size of the ngrams to generate.
    lowercase : bool
        Whether or not to lowercase all tokens.
    cutoff : int
        Perform a cutoff after parsing. We will only return ngrams that have a
        frequency higher than the cutoff.

    Returns
    -------
    NgramMap
        The ngram map that allows you to iterate over the ngrams.
    """
    ngram_map = NgramMap()

    with open(infile, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = preprocess(line)
            ngram_list = []
            tokenizer = ForwardTokenizer(line)
            tokenizer.lowercase = lowercase
            while len(ngram_list) < ngram_size - 1 and tokenizer.has_more_tokens():
                token = tokenizer.next_token()
                if token != "":
                    token_idx = ngram_map.add_token(token)
                    ngram_list.append(token_idx)
            if len(ngram_list) < ngram_size - 1:
                continue

            tokenizer.reset_stream()
            while tokenizer.has_more_tokens():
                token = tokenizer.next_token()
                if token != "":
                    token_idx = ngram_map.add_token(token)
                    ngram_list.append(token_idx)
                    ngram_map.add(ngram_list)
                    ngram_list.pop(0)

    if cutoff > 0:
        ngram_map.cutoff(cutoff)

    return ngram_map
