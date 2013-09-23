# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

"""
Several classes to tokenize text.

"""

import abc
import codecs
import collections

import pressagio.character

class Tokenizer:
    """
    Base class for all tokenizers.

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, stream, blankspaces = pressagio.character.blankspaces,
            separators = pressagio.character.separators):
        """
        Constructor of the Tokenizer base class.

        Parameters
        ----------
        stream : str or io.IOBase
            The stream to tokenize. Can be a filename or any open IO stream.

        blankspaces : str
            The characters that represent empty spaces.

        separators : str
            The characters that separate token units (e.g. word boundaries).

        """
        self.separators = separators
        self.blankspaces = blankspaces
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

    def count_characters(self):
        """
        Counts the number of unicode characters in the IO stream.

        """
        count = 0
        self.stream.seek(0)
        while self.stream.read(1):
            count += 1
        #self.reset_stream()
        self.stream.seek(0)

        return count

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

    def __init__(self, stream, blankspaces = pressagio.character.blankspaces,
            separators = pressagio.character.separators):
        super().__init__(stream, blankspaces, separators)
        self.stream = stream
        if not hasattr(stream, 'read'):
            self.stream = codecs.open(stream, "r", "utf-8")

        self.offend = self.count_characters()
        self.reset_stream()

    def count_tokens(self):
        count = 0
        while(self.has_more_tokens()):
            count += 1
            self.next_token()

        self.reset_stream()
        
        return count

    def has_more_tokens(self):
        if self.offset < self.offend:
            return True
        return False

    def next_token(self):
        current = self.stream.read(1)
        self.offset += 1
        token = ""

        if self.offset < self.offend:
            while self.is_blankspace(current) or self.is_separator(current) \
                    and self.offset <= self.offend:
                current = self.stream.read(1)
                self.offset += 1

            while not self.is_blankspace(current) and not self.is_separator(
                    current) and self.offset <= self.offend:
                if self.lowercase:
                    current = current.lower()

                token += current

                current = self.stream.read(1)
                self.offset += 1

        return token 

    def progress(self):
        return float(offset)/offend

    def reset_stream(self):
        self.stream.seek(0)
        self.offset = 0


class ReverseTokenizer(Tokenizer):

    def __init__(self, stream, blankspaces = pressagio.character.blankspaces,
            separators = pressagio.character.separators):
        super().__init__(stream, blankspaces, separators)
        self.stream = stream
        if not hasattr(stream, 'read'):
            self.stream = open(stream, "rb")

        self.stream.seek(0, 2)
        self.offend = self.stream.tell()
        self.offset = self.offend

    def count_tokens(self):
        curroff = self.offset
        self.offset = self.offend
        count = 0
        while (self.has_more_tokens()):
            self.next_token()
            count += 1
        self.offset = curroff
        return count

    def has_more_tokens(self):
        if (self.offbeg < self.offset):
            return True
        else:
            return False

    def next_token(self):
        token = ""

        while (self.offbeg < self.offset) and len(token) == 0:
            current = self._get_character_at_offset()
            current_width = len(current.encode("utf-8"))

            if (self.offset == self.offend) and (self.is_separator(current) \
                    or self.is_blankspace(current)):
                self.offset -= current_width
                return token

            while (self.is_blankspace(current) or self.is_separator(current)) \
                    and self.offbeg < self.offset:
                self.offset -= current_width
                if (self.offbeg < self.offset):
                    current = self._get_character_at_offset()
                    current_width = len(current.encode("utf-8"))

            while not self.is_blankspace(current) and not self.is_separator(
                current) and self.offbeg < self.offset:
                if self.lowercase:
                    current = current.lower()
                token = current + token
                self.offset -= current_width
                if (self.offbeg < self.offset):
                    current = self._get_character_at_offset()
                    current_width = len(current.encode("utf-8"))

        return token

    def _get_character_at_offset(self):
        current = ""
        was_raised = False
        if self.offset < 8:
            self.stream.seek(0)
            current = self.stream.read(self.offset).decode("utf-8")
        else:
            for start in range(4, 8):
                self.stream.seek(self.offset - start)
                try:
                    current = self.stream.read(start).decode("utf-8")
                except UnicodeDecodeError:
                    pass
                else:
                    break

        char = current[-1]
        return char

    def progress(self):
        return float(self.offend - self.offset) / (self.offend - self.offbeg)

    def reset_stream(self):
        self.stream.seek(0, 2)
        self.offset = self.offend


def forward_tokenize_file(infile, ngram_size, lowercase=False):
    ngram_map = collections.defaultdict(int)
    ngram_list = []
    tokenizer = ForwardTokenizer(infile)
    tokenizer.lowercase = lowercase

    for i in range(ngram_size - 1):
        if not tokenizer.has_more_tokens():
            break
        ngram_list.append(tokenizer.next_token())

    while (tokenizer.has_more_tokens()):
        token = tokenizer.next_token()
        ngram_list.append(token)
        ngram_map[tuple(ngram_list)] += 1
        ngram_list.pop(0)    

    return ngram_map

