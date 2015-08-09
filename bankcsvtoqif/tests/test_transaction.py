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
import csv

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from bankcsvtoqif.tests.test_banks import csvline_to_line
from bankcsvtoqif.transaction import Transaction, TransactionFactory
from bankcsvtoqif.banks import DBGiro


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.csv_line = """22.04.2015;22.04.2015;"SEPA-Überweisung an";\
        Smith, John;Rent;DE12345678909876543212;\
        BYLADEM1GLA;;;;;;;-10,00;;EUR"""
        self.account_config = DBGiro()

    def write_fake_csv(self):
        fake_file = StringIO()
        csv.register_dialect(
            self.account_config.name,
            self.account_config.get_csv_dialect()
        )
        csv_writer = csv.writer(fake_file, 'db_giro')
        csv_writer.writerow(['hello'])
        fake_file.seek(0,0)
        return fake_file

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
        line = csvline_to_line(self.csv_line, self.account_config)
        transaction_factory = TransactionFactory(self.account_config)
        transaction = transaction_factory.create_from_line(line)
        self.assertEqual(transaction.date, self.account_config.get_date(line))
        self.assertEqual(transaction.description, self.account_config.get_description(line))
        self.assertEqual(transaction.debit, self.account_config.get_debit(line))
        self.assertEqual(transaction.credit, self.account_config.get_credit(line))
        self.assertEqual(transaction.account, self.account_config.default_target_account)

    def test_read_from_file(self):
        fake_csv_file = self.write_fake_csv()
        print(fake_csv_file.readline())
