# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

import pressagio.core.predictor

class TestSuggestion():

    def setup(self):
        self.suggestion = pressagio.core.predictor.Suggestion("Test", 0.3)

    def test_probability(self):
        self.suggestion.probability = 0.1
        assert self.suggestion.probability == 0.1


class TestPrediction():

    def setup(self):
        self.prediction = pressagio.core.predictor.Prediction()

    def test_add_suggestion(self):
        self.prediction.add_suggestion(pressagio.core.predictor.Suggestion(
            "Test", 0.3))
        assert self.prediction[0].word == "Test"
        assert self.prediction[0].probability == 0.3

        self.prediction.add_suggestion(pressagio.core.predictor.Suggestion(
            "Test2", 0.2))
        assert self.prediction[0].word == "Test"
        assert self.prediction[0].probability == 0.3
        assert self.prediction[1].word == "Test2"
        assert self.prediction[1].probability == 0.2

        self.prediction.add_suggestion(pressagio.core.predictor.Suggestion(
            "Test3", 0.6))
        assert self.prediction[0].word == "Test3"
        assert self.prediction[0].probability == 0.6
        assert self.prediction[1].word == "Test"
        assert self.prediction[1].probability == 0.3
        assert self.prediction[2].word == "Test2"
        assert self.prediction[2].probability == 0.2

        self.prediction.clear()

    def test_suggestion_for_token(self):
        self.prediction.add_suggestion(pressagio.core.predictor.Suggestion(
            "Token", 0.8))
        assert self.prediction.suggestion_for_token("Token").probability == 0.8
        self.prediction.clear()