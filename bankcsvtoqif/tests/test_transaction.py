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
import csv
from bankcsvtoqif.io import Messenger

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from bankcsvtoqif.tests.banks import csvline_to_line
from bankcsvtoqif.transaction import Transaction, TransactionFactory
from bankcsvtoqif.banks.db_giro import DBGiro

csv_test_file = [
    ['heading', '', '', '', 'heading'],
    ['date'],
    ['balance', '', '', '', '1.2345,67', '', 'EUR'],
    ['some text'],
    ['column heads'],
    ['25.07.2015', '26.07.2015', '', '', 'description1', '', '', '', '', '', '', '', '', '', '-1,23', '', 'EUR'],
    ['27.07.2015', '28.07.2015', '', '', 'description2', '', '', '', '', '', '', '', '', '', '-2,34', '', 'EUR'],
    ['28.07.2015', '29.07.2015', '', '', 'description3', '', '', '', '', '', '', '', '', '', '', '4,56', 'EUR'],
    ['balance', '28.07.2015', '', '', '2.345,67', 'EUR', ],
]

csv_line = """22.04.2015;22.04.2015;"SEPA-Überweisung an";\
        Smith, John;Rent;DE12345678909876543212;\
        BYLADEM1GLA;;;;;;;;-10,00;;EUR"""


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.account_config = DBGiro()

    def test_create_transaction(self):
        date = datetime(2015, 5, 17)
        description = 'milk'
        category = ''
        debit = 1.05
        credit = 0
        target_account = 'Expenses:Groceries'
        transaction = Transaction(date, description, category, debit, credit, target_account)
        self.assertEqual(transaction.date, date)
        self.assertEqual(transaction.description, description)
        self.assertEqual(transaction.category, category)
        self.assertEqual(transaction.debit, debit)
        self.assertEqual(transaction.credit, credit)
        self.assertEqual(transaction.target_account, target_account)
        self.assertEqual(transaction.amount, credit - debit)

    def test_to_qif_line(self):
        date = datetime(2015, 5, 17)
        description = 'milk'
        category = ''
        debit = 1.05
        credit = 0
        target_account = 'Expenses:Groceries'
        t = Transaction(date, description, category, debit, credit, target_account)
        self.assertEqual(len(t.to_qif_line()), 7)


class TestTransactionFactory(unittest.TestCase):

    def setUp(self):
        self.account_config = DBGiro()

    def write_fake_csv(self):
        fake_file = StringIO()
        csv.register_dialect(
            'test_dialect',
            self.account_config.get_csv_dialect()
        )
        csv_writer = csv.writer(fake_file, 'test_dialect')
        for row in csv_test_file:
            csv_writer.writerow(row)
        fake_file.seek(0, 0)
        return fake_file

    def test_create_transaction_factory(self):
        line = csvline_to_line(csv_line, self.account_config)
        transaction_factory = TransactionFactory(self.account_config)
        transaction = transaction_factory.create_from_line(line)
        self.assertEqual(transaction.date, self.account_config.get_date(line))
        self.assertEqual(transaction.description, self.account_config.get_description(line))
        self.assertEqual(transaction.category, self.account_config.get_category(line))
        self.assertEqual(transaction.debit, self.account_config.get_debit(line))
        self.assertEqual(transaction.credit, self.account_config.get_credit(line))
        self.assertEqual(transaction.target_account, self.account_config.default_target_account)

    def test_read_from_file(self):
        fake_csv_file = self.write_fake_csv()
        transaction_factory = TransactionFactory(self.account_config)
        transactions = transaction_factory.read_from_file(fake_csv_file, Messenger(False))
        fake_csv_file.close()
        self.assertEqual(len(transactions),3)
