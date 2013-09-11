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

        self.stream.seek(0, SEEK_END)
        self.offend = self.stream.tell()
        self.stream.seek(0)
        self.offset = self.stream.tell()
        self.offbeg = self.stream.tell()

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

        return count

    def has_more_tokens():
        if self.offset < self.offend:
            return True
        return False

    def next_token(self):
        pass

    def progress(self):
        return float(offset)/offend