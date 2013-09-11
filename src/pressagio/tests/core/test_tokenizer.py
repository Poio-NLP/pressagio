# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

import os
import codecs

import pressagio.core.tokenizer

class TestTokenizer():

    def setup(self):
        filename = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
            '..', 'test_data', 'der_linksdenker.txt'))
        self.tokenizer = pressagio.core.tokenizer.Tokenizer(filename)

    def test_is_blankspace(self):
        assert self.tokenizer.is_blankspace('\n') == True
        assert self.tokenizer.is_blankspace('a') == False

    def test_is_separator(self):
        assert self.tokenizer.is_separator('"') == True
        assert self.tokenizer.is_separator('b') == False
