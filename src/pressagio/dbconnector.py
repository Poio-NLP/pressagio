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
    """
    Base class for all database connectors.

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, dbname, cardinality = 1):
        """
        Constructor of the base class DababaseConnector.

        Parameters
        ----------
        dbname : str
            path to the database file or database name
        cardinality : int
            default cardinality for n-grams

        """
        self.cardinality = cardinality
        self.dbname = dbname

    def create_ngram_table(self, cardinality):
        """
        Creates a table for n-gram of a give cardinality. The table name is
        constructed from this parameter, for example for cardinality `2` there
        will be a table `_2_gram` created.

        Parameters
        ----------
        cardinality : int
            The cardinality to create a table for.

        """

        query = "CREATE TABLE IF NOT EXISTS _{0}_gram (".format(cardinality)
        unique = ""
        for i in reversed(range(cardinality)):
            if i != 0:
                unique += "word_{0}, ".format(i)
                query += "word_{0} TEXT, ".format(i)
            else:
                unique += "word"
                query += "word TEXT, count INTEGER, UNIQUE({0}) );".format(
                    unique)

        self.execute_sql(query)

    def create_unigram_table(self):
        """
        Creates a table for n-grams of cardinality 1.

        """
        self.create_ngram_table(1)

    def create_bigram_table(self):
        """
        Creates a table for n-grams of cardinality 2.

        """
        self.create_ngram_table(2)

    def create_trigram_table(self):
        """
        Creates a table for n-grams of cardinality 3.

        """
        self.create_ngram_table(3)

    def unigram_count_sum(self):
        pass

    def ngram_count(self, ngram):
        query = "SELECT count FROM _{0}_gram".format(len(ngram))
        query += self._build_where_clause(ngram)
        query += ";"

        result = self.execute_sql(query)

        return self._extract_first_integer(result)

    def ngram_like_table(self, ngram, limit = -1):
        pass

    def ngram_like_table_filtered(self, ngram, filter, limit = -1):
        pass

    def increment_ngram_count(self, ngram):
        pass

    def insert_ngram(self, ngram, count):
        """
        Inserts a given n-gram with count into the database.

        ngram : iterable of str
            A list, set or tuple of strings.
        count : int
            The count for the given n-gram.

        """
        query = "INSERT INTO _{0}_gram {1};".format(len(ngram),
            self._build_values_clause(ngram, count))
        self.execute_sql(query)

    def update_ngram(self, ngram, count):
        query = "UPDATE _{0}_gram SET count = {1}".format(len(ngram), count)
        query += self._build_where_clause(ngram)
        query += ";"
        self.execute_sql(query)

    def remove_ngram(self, ngram):
        pass

    def open_database(self):
        raise NotImplementedError("Method must be implemented")

    def close_database(self):
        raise NotImplementedError("Method must be implemented")

    def execute_sql(self):
        raise NotImplementedError("Method must be implemented")

    ############################################### Private methods

    def _build_values_clause(self, ngram, count):
        values_clause = "VALUES('"
        values_clause += "', '".join(ngram)
        values_clause += "', {0})".format(count)
        return values_clause

    def _build_where_clause(self, ngram):
        where_clause = " WHERE"
        for i, n in enumerate(ngram):
            if i < (len(ngram) - 1):
                where_clause += " word_{0} = '{1}' AND".format(len(ngram)-1, n)
            else:
                where_clause += " word = '{0}'".format(n)
        return where_clause

    def _extract_first_integer(self, table):
        count = 0
        if len(table) > 0:
            if len(table[0]) > 0:
                count = int(table[0][0])

        if not count > 0:
            count = 0
        return count


class SqliteDatabaseConnector(DatabaseConnector):
    """
    Database connector for sqlite databases.

    """

    def __init__(self, dbname, cardinality = 1):
        """
        Constructor for the sqlite database connector.

        Parameters
        ----------
        dbname : str
            path to the database file or database name
        cardinality : int
            default cardinality for n-grams

        """
        super().__init__(dbname, cardinality)
        self.con = None
        self.open_database()

    def __del__(self):
        self.close_database()

    def commit(self):
        self.con.commit()
        
    def open_database(self):
        """
        Opens the sqlite database.

        """
        self.con = sqlite3.connect(self.dbname)

    def close_database(self):
        """
        Closes the sqlite database.

        """
        if self.con:
            self.con.close()

    def execute_sql(self, query):
        """
        Executes a given query string on an open sqlite database.

        """
        c = self.con.cursor()
        c.execute(query)
        result = c.fetchall()
        return result