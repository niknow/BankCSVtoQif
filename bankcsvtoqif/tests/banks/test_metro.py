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
from bankcsvtoqif.tests.banks import csvline_to_line

from bankcsvtoqif.banks.metro import Metro


class TestMetro(unittest.TestCase):

    def setUp(self):
        self.csv = """26/01/2018,Savings account,Outward Faster Payment,0.00,12.34,56.78"""
        self.csv2 = """26/01/2018,Acme Ltd Pay,Inward Payment,1000.00,0.00,1056.78.00"""

    def test_can_instantiate(self):
        account_config = Metro()
        self.assertEqual(type(account_config), Metro)

    def test_debit(self):
        account_config = Metro()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2018, 1, 26)
        description = 'Savings account'
        debit = 12.34
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)

    def test_credit(self):
        account_config = Metro()
        line = csvline_to_line(self.csv2, account_config)
        date = datetime(2018, 1, 26)
        description = 'Acme Ltd Pay'
        debit = 0
        credit = 1000.00
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
