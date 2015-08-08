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
import tempfile
import os
import json

from bankcsvtoqif.smartlabeler import Replacement
from bankcsvtoqif.transaction import Transaction
from bankcsvtoqif.smartlabeler import SmartLabeler

replacements = {
    "db_giro": [
        ["no123", "rent", "Expenses:Rent", 1],
        ["xyz", "ice cream", "Expenses:Sweeties", 0],
    ]
}


class TestReplacement(unittest.TestCase):
    def setUp(self):
        self.replacement0 = Replacement('Rent', 'Rent', 'Expenses:Rent', 0)
        self.replacement1 = Replacement('Rent', 'Rent', 'Expenses:Rent', 1)
        self.replacement2 = Replacement('Rent', 'Rent', 'Expenses:Rent', 2)

    def test_replacement_matches(self):
        self.assertEqual(self.replacement1.matches('Rent'), True)

    def test_replacement_should_append_date(self):
        self.assertEqual(self.replacement0.should_append_date(), False)
        self.assertEqual(self.replacement1.should_append_date(), True)
        self.assertEqual(self.replacement2.should_append_date(), True)

    def test_replacement_should_append_next_month_date(self):
        self.assertEqual(self.replacement0.should_append_next_month_date(), False)
        self.assertEqual(self.replacement1.should_append_next_month_date(), False)
        self.assertEqual(self.replacement2.should_append_next_month_date(), True)

    def test_replacement_get_description(self):
        date = datetime(2015, 5, 1)
        self.assertEqual(self.replacement0.get_description(date), 'Rent')
        self.assertEqual(self.replacement1.get_description(date), 'Rent 2015-05')
        self.assertEqual(self.replacement2.get_description(date), 'Rent 2015-06')


class TestSmartLabeler(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction(datetime(2015, 5, 1), 'RentXYZ234 3848267', 500, 0, 'Imbalance-EUR')
        self.replacement1 = Replacement('Rent', 'Rent', 'Expenses:Rent', 0)
        self.replacement2 = Replacement('Rent', '', 'Expenses:Rent', 0)
        self.SmartLabeler = SmartLabeler()

    def test_has_replacement(self):
        self.assertEqual(bool(self.SmartLabeler.has_replacement(self.transaction)), False)
        self.SmartLabeler.replacements.append(self.replacement1)
        self.assertEqual(self.SmartLabeler.has_replacement(self.transaction), self.replacement1)

    def test_replace(self):
        replaced_transaction = self.SmartLabeler.replace(self.transaction, self.replacement1)
        self.assertEqual(replaced_transaction.description, self.replacement1.new_description)
        self.assertEqual(replaced_transaction.account, self.replacement1.account)
        replaced_transaction = self.SmartLabeler.replace(self.transaction, self.replacement2)
        self.assertEqual(replaced_transaction.description, self.transaction.description)
        self.assertEqual(replaced_transaction.account, self.replacement2.account)

    def test_load_replacements_from_file(self):
        self.replacements_file = tempfile.mkstemp(dir='.')
        f = os.fdopen(self.replacements_file[0], 'w')
        json.dump(replacements, f)
        f.close()
        self.SmartLabeler.load_replacements_from_file(self.replacements_file[1], 'db_giro')
        self.assertEqual(len(self.SmartLabeler.replacements), 2)
        os.remove(self.replacements_file[1])
