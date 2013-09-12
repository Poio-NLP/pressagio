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
        filename = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
            '..', 'test_data', 'test.db'))
        self.connector = pressagio.dbconnector.SqliteDatabaseConnector(filename)

    def test_open_database(self):
        self.connector.open_database()

    def test_close_database(self):
        self.connector.close_database()
