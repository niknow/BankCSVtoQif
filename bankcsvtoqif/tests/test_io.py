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

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import unittest
from datetime import datetime

from bankcsvtoqif.io import DataManager
from bankcsvtoqif.banks.db_giro import DBGiro
from bankcsvtoqif.transaction import Transaction


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.account_config = DBGiro()

    def test_create_data_manager(self):
        d = DataManager('', '', '', self.account_config, False)
        self.assertEqual(len(d.transactions), 0)

    def test_read_csv(self):
        d = DataManager('', '', '', self.account_config, False)
        d.read_csv(StringIO())
        self.assertEqual(len(d.transactions), 0)

    def test_relabel_transactions(self):
        d = DataManager('', '', '', self.account_config, False)
        d.read_csv(StringIO())
        self.assertEqual(len(d.transactions), 0)

    def test_write_qif(self):
        d = DataManager('', '', '', self.account_config, False)
        fake_qif = StringIO()
        d.transactions.append(Transaction(datetime(2015, 5, 1), 'RentXYZ234 3848267', 500, 0, 'Imbalance-EUR'))
        d.write_qif(fake_qif)
        fake_qif.seek(0, 0)
        self.assertEqual(len(fake_qif.readlines()), 9)
        fake_qif.close()
