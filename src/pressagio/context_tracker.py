# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

"""
Class for context tracker.

"""

import copy

import pressagio.character
import pressagio.observer

DEFAULT_SLIDING_WINDOW_SIZE = 80

class ContextChangeDetector:

    def __init__(self, lowercase):
        self.lowercase = lowercase
        self.sliding_windows_size = DEFAULT_SLIDING_WINDOW_SIZE
        self.sliding_window = ""

    def update_sliding_window(self, string):
        if len(string) <= self.sliding_windows_size:
            self.sliding_window = string
        else:
            self.sliding_window = string[:-self.sliding_windows_size]

    def context_change(self, past_stream):
        # rename for clarity
        prev_context = self.sliding_window
        curr_context = past_stream

        if len(prev_context) == 0:
            if len(curr_context) == 0:
                return False
            else:
                return True

        ctx_idx = curr_context.rfind(prev_context)
        if ctx_idx == -1:
            return True

        remainder = curr_context[ctx_idx + len(prev_context):]
        idx = pressagio.character.last_word_character(remainder)
        if idx == -1:
            if len(remainder) == 0:
                return False
            last_char = curr_context[ctx_idx + len(prev_context) - 1]
            if pressagio.character.is_word_character(last_char):
                return False
            else:
                return True

        if idx == len(remainder) - 1:
            return False

        return True

    def change(self, past_stream):
        # rename for clarity
        prev_context = self.sliding_window
        curr_context = past_stream

        if len(prev_context) == 0:
            return past_stream

        ctx_idx = curr_context.rfind(prev_context)
        if ctx_idx == -1:
            return past_stream

        result = curr_context[ctx_idx + len(prev_context):]
        if (self.context_change(past_stream)):
            sliding_window_stream = self.sliding_window
            r_tok = pressagio.tokenizer.ReverseTokenizer(sliding_window_stream)
            r_tok.lowercase = self.lowercase
            first_token = r_tok.next_token()
            if not len(first_token) == 0:
                result = first_token + result

        return result

class ContextTracker(pressagio.observer.Observer):
    """
    Tracks the current context.

    """

    def __init__(self, config, predictor_registry, callback, word_chars,
            separator_chars, blankspace_chars, control_chars):
        self.dispatcher = pressagio.observer.Dispatcher(self) 