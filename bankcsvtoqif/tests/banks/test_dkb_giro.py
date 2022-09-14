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

from bankcsvtoqif.banks.dkb_giro import DKBGiro


class TestDKBGiro(unittest.TestCase):

    def setUp(self):
        self.csv = """21.06.2017;;Kartenzahlung;Geschäft;Ticket;;;-13,50;;;;"""

    def test_can_instantiate(self):
        account_config = DKBGiro()
        self.assertEqual(type(account_config), DKBGiro)

    def test_getters(self):
        account_config = DKBGiro()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 21)
        description = 'Kartenzahlung Geschäft Ticket'
        debit = 13.5
        credit = 0
        all_lines = (line, line)
        self.assertEqual(account_config.get_date(line, all_lines), date)
        self.assertEqual(account_config.get_description(line, all_lines), description)
        self.assertEqual(account_config.get_debit(line, all_lines), debit)
        self.assertEqual(account_config.get_credit(line, all_lines), credit)
