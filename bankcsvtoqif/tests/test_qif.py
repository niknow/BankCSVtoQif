# -*- coding: utf-8 -*-


# BankCSVtoQif - Smart conversion of csv files from a bank to qif
# Copyright (C) 2015-2016  Nikolai Nowaczyk
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
from datetime import datetime
from bankcsvtoqif.qif import QifFile
from bankcsvtoqif.transaction import Transaction


class TestQif(unittest.TestCase):
    def setUp(self):
        self.date = datetime(2015, 5, 1)
        self.account = 'Assets:CurrentAssets:Checking Account'
        self.description = 'icecream'
        self.amount = - 2.50

    def test_create_qif(self):
        q = QifFile(self.account)
        self.assertEqual(q.account, self.account)

    def test_get_raw_data(self):
        q = QifFile(self.account)
        t = Transaction(self.date, self.description, 0, self.amount, 'Expenses:Rent')
        lines = [
            '!Account',
            'N' + self.account,
            '^'
        ]
        lines += t.to_qif_line()
        self.assertEqual(lines, q.get_raw_data([t]))
