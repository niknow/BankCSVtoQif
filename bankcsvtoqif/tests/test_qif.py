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
from datetime import datetime
from bankcsvtoqif.qif import Transaction, Qif


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.date = datetime(2015,5,1)
        self.account = 'Assets:CurrentAssets:Checking Account'
        self.description = 'icecream'
        self.amount = - 2.50

    def test_create_transaction(self):
        t = Transaction(self.date, self.account, self.description, self.amount)
        self.assertEqual(self.date, t.date)
        self.assertEqual(self.account, t.account)
        self.assertEqual(self.description, t.description)
        self.assertEqual(self.amount, t.amount)

    def test_get_lines(self):
        t = Transaction(self.date, self.account, self.description, self.amount)
        self.assertEqual(len(t.get_lines()), 6)


class TestQif(unittest.TestCase):

    def setUp(self):
        self.date = datetime(2015,5,1)
        self.account = 'Assets:CurrentAssets:Checking Account'
        self.description = 'icecream'
        self.amount = - 2.50

    def test_create_qif(self):
        account = 'Assets:Current Assets:Checking Account'
        q = Qif(account)
        t = Transaction(self.date, self.account, self.description, self.amount)
        q.add_transaction(t)
        self.assertEqual(q.account, account)
        self.assertEqual(len(q.transactions), 1)

