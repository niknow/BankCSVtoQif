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

from bankcsvtoqif.banks.orico import Orico
from bankcsvtoqif.tests.banks import csvline_to_line


class TestOrico(unittest.TestCase):

    def setUp(self):
        self.csv = r"""2021年3月1日,This is a debit テスト,null,家族,2021年3月,アド,,,"\-4,000",,,,-,-"""
        self.csv2 = r'''2021年3月10日,This is a credit テスト,*,本人,2021年3月,アド,1,1,"\5,000",,,"\0","\5,000","\0"'''

    def test_can_instantiate(self):
        account_config = Orico()
        self.assertEqual(type(account_config), Orico)

    def test_debit(self):
        account_config = Orico()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2021, 3, 1)
        description = 'This is a debit テスト'
        debit = 4000
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)

    def test_credit(self):
        account_config = Orico()
        line = csvline_to_line(self.csv2, account_config)
        date = datetime(2021, 3, 10)
        description = 'This is a credit テスト'
        debit = 0
        credit = 5000
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
