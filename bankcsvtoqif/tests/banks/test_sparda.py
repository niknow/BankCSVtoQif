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
from bankcsvtoqif.tests.banks import csvline_to_line

from bankcsvtoqif.banks.sparda import SpardaBank


class TestSpardaBank(unittest.TestCase):

    def setUp(self):
        self.csv = """22.04.2015;22.04.2015;\
        "SEPA-Überweisung an Smith, John Rent DE12345678909876543212";\
        -10,00;EUR;ATargetAccount"""

    def test_can_instantiate(self):
        account_config = SpardaBank()
        self.assertEqual(type(account_config), SpardaBank)

    def test_getters(self):
        account_config = SpardaBank()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2015, 4, 22)
        description = 'SEPA-Überweisung an Smith, John Rent DE12345678909876543212'
        targetAccount = 'ATargetAccount'
        debit = 10
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), targetAccount)
