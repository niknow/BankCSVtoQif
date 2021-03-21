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

from bankcsvtoqif.banks.comdirect_visa import ComdirectVisa


class TestComdirectVisa(unittest.TestCase):

    def setUp(self):
        self.csv  = """"01.04.2019";"17.04.2019";"Visa-Umsatz";"123456789";"some debit";"-83,00";"""
        self.csv2 = """"02.04.2019";"18.11.2018";"Visa-Umsatz";"123456789";"some credit";"123,45";"""

    def test_can_instantiate(self):
        account_config = ComdirectVisa()
        self.assertEqual(type(account_config), ComdirectVisa)

    def test_debit(self):
        account_config = ComdirectVisa()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2019, 4, 17)
        description = 'some debit'
        debit = 83.0
        credit = 0
        all_lines = (line, line)
        self.assertEqual(account_config.get_date(line, all_lines), date)
        self.assertEqual(account_config.get_description(line, all_lines), description)
        self.assertEqual(account_config.get_debit(line, all_lines), debit)
        self.assertEqual(account_config.get_credit(line, all_lines), credit)

    def test_credit(self):
        account_config = ComdirectVisa()
        line = csvline_to_line(self.csv2, account_config)
        date = datetime(2018, 11, 18)
        description = 'some credit'
        debit = 0
        credit = 123.45
        all_lines = (line, line)
        self.assertEqual(account_config.get_date(line, all_lines), date)
        self.assertEqual(account_config.get_description(line, all_lines), description)
        self.assertEqual(account_config.get_debit(line, all_lines), debit)
        self.assertEqual(account_config.get_credit(line, all_lines), credit)
