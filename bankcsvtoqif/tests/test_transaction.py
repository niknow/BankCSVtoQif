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
from .test_banks import csvline_to_line
from ..transaction import Transaction, TransactionFactory
from ..banks import DBGiro


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.csv_line = """22.04.2015;22.04.2015;"SEPA-Überweisung an";\
        Smith, John;Rent;DE12345678909876543212;\
        BYLADEM1GLA;;;;;;;-10,00;;EUR"""
    
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
        account_config = DBGiro()
        line = csvline_to_line(self.csv_line, account_config)
        transaction_factory = TransactionFactory(account_config)
        transaction = transaction_factory.create_from_line(line)
        self.assertEqual(transaction.date, account_config.get_date(line))
        self.assertEqual(transaction.description, account_config.get_description(line))
        self.assertEqual(transaction.debit, account_config.get_debit(line))
        self.assertEqual(transaction.credit, account_config.get_credit(line))
        self.assertEqual(transaction.account, account_config.default_target_account)
