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
from transaction import Transaction, TransactionFactory
import banks
from datetime import datetime
import csv
from smartlabeler import Replacement

db_giro_csv1 = """22.04.2015;22.04.2015;"SEPA-Überweisung an";\
    Smith, John;Rent;DE12345678909876543212;\
    BYLADEM1GLA;;;;;;;-10,00;;EUR"""


class BankCSVtoQifTest(unittest.TestCase):

    # --- test setup and tear down ---
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --- helper functions ---

    def csvline_to_line(self, csvline, account_config):
        csvline = csvline.splitlines()
        csv.register_dialect(
            account_config.name,
            delimiter=account_config.delimiter,
            quotechar=account_config.quotechar
        )
        c = csv.reader(csvline, account_config.name)
        return next(c)

    # --- tests ---

    # banks.py

    def test_db_giro(self):
        account_config = banks.DBGiro()
        line = self.csvline_to_line(db_giro_csv1, account_config)
        date = datetime(2015, 4, 22)
        description = 'SEPA-Überweisung an Smith, John Rent'
        debit = 10
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)

    # class Transaction
    def test_create_transaction(self):
        date = datetime(2015, 5, 17)
        description = 'milk'
        debit = 1.05
        credit = 0
        account = 'Expenses:Groceries'
        transaction = Transaction(date, description, debit, credit, account)
        self.assertEqual(transaction.date, date)
        self.assertEqual(transaction.description, description)
        self.assertEqual(transaction.debit, debit)
        self.assertEqual(transaction.credit, credit)
        self.assertEqual(transaction.account, account)
        self.assertEqual(transaction.amount, credit - debit)

    def test_transaction_factory(self):
        account_config = banks.DBGiro()
        line = self.csvline_to_line(db_giro_csv1, account_config)
        transaction_factory = TransactionFactory(account_config)
        transaction = transaction_factory.create_from_line(line)
        self.assertEqual(transaction.date, account_config.get_date(line))
        self.assertEqual(transaction.description, account_config.get_description(line))
        self.assertEqual(transaction.debit, account_config.get_debit(line))
        self.assertEqual(transaction.credit, account_config.get_credit(line))
        self.assertEqual(transaction.account, account_config.default_target_account)

    def test_replacement_matches(self):
        replacement = Replacement('Rent', 'Rent', 'Expenses:Rent', 1)
        self.assertEqual(replacement.matches('Rent'), True)

    def test_replacement_should_append_date(self):
        replacement0 = Replacement('Rent', 'Rent', 'Expenses:Rent', 0)
        replacement1 = Replacement('Rent', 'Rent', 'Expenses:Rent', 1)
        replacement2 = Replacement('Rent', 'Rent', 'Expenses:Rent', 2)
        self.assertEqual(replacement0.should_append_date(), False)
        self.assertEqual(replacement1.should_append_date(), True)
        self.assertEqual(replacement2.should_append_date(), True)

    def test_replacement_should_append_next_month_date(self):
        replacement0 = Replacement('Rent', 'Rent', 'Expenses:Rent', 0)
        replacement1 = Replacement('Rent', 'Rent', 'Expenses:Rent', 1)
        replacement2 = Replacement('Rent', 'Rent', 'Expenses:Rent', 2)
        self.assertEqual(replacement0.should_append_next_month_date(), False)
        self.assertEqual(replacement1.should_append_next_month_date(), False)
        self.assertEqual(replacement2.should_append_next_month_date(), True)

    def test_replacement_get_description(self):
        replacement0 = Replacement('RentXYZ', 'Rent', 'Expenses:Rent', 0)
        replacement1 = Replacement('RentXYZ', 'Rent', 'Expenses:Rent', 1)
        replacement2 = Replacement('RentXYZ', 'Rent', 'Expenses:Rent', 2)
        replacement3 = Replacement('RentXYZ', '', 'Expenses:Rent', 2)
        date = datetime(2015,5,1)
        self.assertEqual(replacement0.get_description(date), 'Rent')
        self.assertEqual(replacement1.get_description(date), 'Rent 2015-05')
        self.assertEqual(replacement2.get_description(date), 'Rent 2015-06')
        self.assertEqual(replacement3.get_description(date), 'RentXYZ')


# if __name__ == '__main__':
# unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(BankCSVtoQifTest)
unittest.TextTestRunner(verbosity=2).run(suite)
