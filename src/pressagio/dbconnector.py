# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2001-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE

"""
Classes to connect to databases.

"""
import abc
import sqlite3

class DatabaseConnector():

    __metaclass__ = abc.ABCMeta

    def __init__(self, dbname, cardinality = 1, read_write = True):
        self.cardinality = cardinality
        self.dbname = dbname

    def create_ngram_table(self, cardinality):
        pass

    def create_unigram_table(self):
        self.create_ngram_table(1)

    def create_bigram_table(self):
        self.create_ngram_table(2)

    def create_trigram_table(self):
        self.create_ngram_table(3)

    def unigram_count_sum(self):
        pass

    def ngram_count(self, ngram):
        pass

    def ngram_like_table(self, ngram, limit = -1):
        pass

    def ngram_like_table_filtered(self, ngram, filter, limit = -1):
        pass

    def increment_ngram_count(self, ngram):
        pass

    def insert_ngram(self, ngram):
        pass

    def update_ngram(self, ngram):
        pass

    def remove_ngram(self, ngram):
        pass

    def open_database(self):
        raise NotImplementedError("Method must be implemented")

    def close_database(self):
        raise NotImplementedError("Method must be implemented")

    def execute_sql(self):
        raise NotImplementedError("Method must be implemented")


class SqliteDatabaseConnector(DatabaseConnector):

    def __init__(self, dbname, cardinality = 1, read_write = True):
        super().__init__(dbname, cardinality, read_write)
        self.con = None

    def open_database(self):
        self.con = sqlite3.connect(self.dbname)

    def close_database(self):
        if self.con:
            self.con.close()