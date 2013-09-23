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

class Tokenizer:
    """
    Base class for all tokenizers.

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, stream, blankspaces = " \f\n\r\t\v",
            separators = "`~!@#$%^&*()_-+=\\|]}[{'\";:/?.>,<"):
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

        self.stream = stream
        if not hasattr(stream, 'read'):
            self.stream = codecs.open(stream, "r", "utf-8")

        self.offset = 0
        self.offend = self.count_characters()

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
        while self.stream.read(1):
            count += 1

        self.reset_stream()

        return count

    def reset_stream(self):
        self.stream.seek(0)
        self.offset = 0

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
                    and self.offset < self.offend:
                current = self.stream.read(1)
                self.offset += 1

            while not self.is_blankspace(current) and not self.is_separator(current) \
                    and self.offset < self.offend:
                if self.lowercase:
                    current = current.lower()

                token += current

                current = self.stream.read(1)
                self.offset += 1

        return token 

    def progress(self):
        return float(offset)/offend

def tokenize_file(infile, ngram_size, lowercase=False):
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