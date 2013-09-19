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
import pressagio.core.observer

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
        if len(self.sliding_window) == 0:
            if len(past_stream) == 0:
                return False
            else:
                return True

        ctx_idx = past_stream.rfind(self.sliding_window)
        if ctx_idx == -1:
            return True

        remainder = past_stream[ctx_idx + len(self.sliding_window):]
        idx = pressagio.character.last_word_character(remainder)
        if idx == -1:
            if len(remainder) == 0:
                return False
            last_char = past_stream[ctx_idx + len(self.sliding_window) - 1]
            if pressagio.character.is_word_character(last_char):
                return False
            else:
                return True

        if idx == len(remainder) - 1:
            return False

        return True


class ContextTracker(pressagio.core.observer.Observer):
    """
    Tracks the current context.

    """

    def __init__(self, config, predictor_registry, callback, word_chars,
            separator_chars, blankspace_chars, control_chars):
        self.dispatcher = pressagio.core.observer.Dispatcher(self) 