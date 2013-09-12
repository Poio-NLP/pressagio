# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2001-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE

import os

import pressagio.dbconnector

class TestSqliteDatabaseConnector():

    def setup(self):
        self.filename = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
            'test_data', 'test.db'))
        self.connector = pressagio.dbconnector.SqliteDatabaseConnector(self.filename)
        self.connector.open_database()

    def test_execute_sql(self):
        self.connector.execute_sql("CREATE TABLE IF NOT EXISTS test ( c1 TEXT, c2 INTEGER );")

    def test_create_ngram_table(self):
        self.connector.create_ngram_table(1)
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_1_gram';")
        assert result == [('_1_gram',)]
        self.connector.execute_sql("DROP TABLE _1_gram;")

        self.connector.create_ngram_table(2)
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_2_gram';")
        assert result == [('_2_gram',)]
        self.connector.execute_sql("DROP TABLE _2_gram;")

        self.connector.create_ngram_table(3)
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_3_gram';")
        assert result == [('_3_gram',)]
        self.connector.execute_sql("DROP TABLE _3_gram;")

    def test_create_unigram_table(self):
        self.connector.create_unigram_table()
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_1_gram';")
        assert result == [('_1_gram',)]
        self.connector.execute_sql("DROP TABLE _1_gram;")

    def test_create_bigram_table(self):
        self.connector.create_bigram_table()
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_2_gram';")
        assert result == [('_2_gram',)]
        self.connector.execute_sql("DROP TABLE _2_gram;")

    def test_create_trigram_table(self):
        self.connector.create_trigram_table()
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_3_gram';")
        assert result == [('_3_gram',)]
        self.connector.execute_sql("DROP TABLE _3_gram;")

    def test_insert_ngram(self):
        self.connector.create_bigram_table()
        self.connector.insert_ngram(('der', 'linksdenker'), 22)
        result = self.connector.execute_sql("SELECT * FROM _2_gram")
        assert result == [('der', 'linksdenker', 22)]
        self.connector.execute_sql("DROP TABLE _2_gram;")

    def teardown(self):
        self.connector.close_database()
        if os.path.isfile(self.filename):
            os.remove(self.filename)
