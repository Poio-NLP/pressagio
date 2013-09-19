# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

"""
Classes for predictors and to handle suggestions and predictions.

"""

import pressagio.core.observer

MIN_PROBABILITY = 0.0
MAX_PROBABILITY = 1.0

class SuggestionException(Exception): pass
class UnknownCombinerException(Exception): pass
class PredictorRegistryException(Exception): pass

class Suggestion:
    """
    Class for a simple suggestion, consists of a string and a probility for that
    string.

    """

    def __init__(self, word, probability):
        self.word = word
        self._probability = probability

    def __eq__(self, other):
        if self.word == other.word and self.probability == other.probability:
            return True
        return False

    def __lt__(self, other):
        if self.probability < other.probability:
            return True
        if self.probability == other.probability:
            return self.word < other.word
        return False

    def __repr__(self):
        return "Word: {0} - Probability: {1}".format(
            self.word, self.probability)


    def probability():
        doc = "The probability property."
        def fget(self):
            return self._probability
        def fset(self, value):
            if value < MIN_PROBABILITY or value > MAX_PROBABILITY:
                raise SuggestionException("Probability is too high or too low.")
            self._probability = value
        def fdel(self):
            del self._probability
        return locals()
    probability = property(**probability())


class Prediction(list):
    """
    Class for predictions from predictors.

    """

    def __init__(self):
        pass

    def __eq__(self, other):
        if self is other:
            return True
        if len(self) != len(other):
            return False
        for i, s in enumerate(other):
            if s != self[i]:
                return False
        return True

    def suggestion_for_token(self, token):
        for s in self:
            if s.word == token:
                return s

    def add_suggestion(self, suggestion):
        if len(self) == 0:
            self.append(suggestion)
        else:
            i = 0
            while i < len(self) and suggestion < self[i]:
                i += 1

            self.insert(i, suggestion)


class PredictorActivator(pressagio.core.observer.Observer)
    """
    PredictorActivator starts the execution of the active predictors,
    monitors their execution and collects the predictions returned, or
    terminates a predictor's execution if it execedes its maximum
    prediction time.

    The predictions returned by the individual predictors are combined
    into a single prediction by the active Combiner.

    """

    def __init__(self, config, registry, context_tracker):
        self.config = config
        self.registry = registry
        self.context_tracker = context_tracker
        self.dispatcher = pressagio.core.observer.Dispatcher(self)
        self.predictions = []

        self.combiner = None
        self.max_partial_prediction_size = None
        self.predict_time = None
        self._combination_policy = None

    def combination_policy():
        doc = "The combination_policy property."
        def fget(self):
            return self._combination_policy
        def fset(self, value):
            self._combination_policy = value
            if value.lower() == "meritocracy":
                self.combiner = pressagio.core.combiner.MeritocracyCombiner()
            else:
                raise UnknownCombinerException()
        def fdel(self):
            del self._combination_policy
        return locals()
    combination_policy = property(**combination_policy())

    def predict(self, multiplier, prediction_filter):
        self.predictions.clear()
        for predictor in self.registry:
            predictions.append(predictor.predict(
                self.max_partial_prediction_size * multiplier,
                prediction_filter))
        result = self.combiner.combine(predictions)
        return result

    def update(self, variable):
        self.dispatcher.dispatch(variable)


class PredictorRegistry(pressagio.core.observer.Observer, list):
    """
    Manages instantiation and iteration through predictors and aids in
    generating predictions and learning.
 
    PredictorRegitry class holds the active predictors and provides the
    interface required to obtain an iterator to the predictors.
 
    The standard use case is: Predictor obtains an iterator from
    PredictorRegistry and invokes the predict() or learn() method on each
    Predictor pointed to by the iterator.
 
    Predictor registry should eventually just be a simple wrapper around
    plump.

    """

    def __init__(self, config):
        self.config = config
        self.predictors_list = []
        self.dispatcher = pressagio.core.observer.Dispatcher(self)
        self._context_tracker = None

    def context_tracker():
        doc = "The context_tracker property."
        def fget(self):
            return self._context_tracker
        def fset(self, value):
            if self._context_tracker is not value:                
                self._context_tracker = value
                self.clear()
                self.set_predictors(self.predictor_list)
        def fdel(self):
            del self._context_tracker
        return locals()
    context_tracker = property(**context_tracker())

    def set_predictors(self, predictors_names):
        self.predictor_list = predictors
        if (self.context_tracker):
            self.clear()
            for predictor in predictors_names:
                self.add_predictor(p)

    def add_predictor(self, predictor_name):
        pass

    def update(self, variable):
        self.dispatcher.dispatch(variable)


class Predictor:
    """
    Base class for predictors.

    """

    def __init__(self, config, context_tracker, predictor_name,
            short_desc = None, long_desc = None):
        self.short_description = short_desc
        self.long_description = long_desc
        self.context_tracker = context_tracker
        self.name = predictor_name
        self.config = config

    def token_satifies_filter(token, prefix, token_filter):
        if token_filter:
            for char in token_filter:
                candidate = prefix + char
                if token.startswith(candidate):
                    return True
        return False

class SmoothedNgramPredictor(Predictor, pressagio.core.observer.Observer):
    """
    Calculates prediction from n-gram model in sqlite database. You have to
    create a database with the script `text2ngram` first.

    """

    def __init__(self, config, context_tracker, predictor_name,
            short_desc = None, long_desc = None):
        Predictor.__init__(config, context_tracker, predictor_name,
            short_desc, long_desc)
        self.db = None
        self.cardinality = None
        self.learn_mode = False
        self.dispatcher = pressagio.core.observer.Dispatcher(self)