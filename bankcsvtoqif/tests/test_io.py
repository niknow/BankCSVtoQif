# -*- coding: utf-8 -*-


# BankCSVtoQif - Smart conversion of csv files from a bank to qif
# Copyright (C) 2015  Nikolai Nowaczyk
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import unittest
import tempfile
import os
from bankcsvtoqif.io import DataManager
from bankcsvtoqif.banks import DBGiro


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.csv_file = tempfile.mkstemp(dir='.')
        self.qif_filename = tempfile.mkstemp(dir='.')
        self.replacements_file = tempfile.mkstemp(dir='.')
        self.account_config = DBGiro()

    def tearDown(self):
        os.close(self.csv_file[0])
        os.close(self.qif_filename[0])
        os.close(self.replacements_file[0])
        os.remove(self.csv_file[1])
        os.remove(self.qif_filename[1])
        os.remove(self.replacements_file[1])

    def test_create_data_manager(self):
        d = DataManager(
            self.csv_file,
            self.qif_filename,
            self.replacements_file,
            self.account_config,
            False
        )
        self.assertEqual(len(d.transactions), 0)
