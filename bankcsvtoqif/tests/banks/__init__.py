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

import csv
import unittest
from pathlib import Path

from bankcsvtoqif.io import Messenger
from bankcsvtoqif.transaction import TransactionFactory


def csvline_to_line(csvline, account_config):
    csvline = csvline.splitlines()
    csv.register_dialect(
        'test_dialect',
        account_config.get_csv_dialect()
    )
    c = csv.reader(csvline, 'test_dialect')
    return next(c)


class TestBankAccountConfig(unittest.TestCase):
    def assert_csv_parsed_as(self, csv_filename, account_config, expected_transactions):
        csv_path = Path(__file__, '..', csv_filename).resolve()
        with csv_path.open("r", newline="", encoding=account_config.encoding) as f:
            factory = TransactionFactory(account_config)
            transactions = factory.read_from_file(f, Messenger(on=False))
        self.assertEqual(
            len(transactions),
            len(expected_transactions),
            "expected {} transactions, received {}".format(
                len(expected_transactions),
                len(transactions)
            )
        )
        for transaction, expected_transaction in zip(transactions, expected_transactions):
            self.assertEqual(transaction.date, expected_transaction.date)
            self.assertEqual(transaction.description, expected_transaction.description)
            self.assertEqual(transaction.debit, expected_transaction.debit)
            self.assertEqual(transaction.credit, expected_transaction.credit)
            self.assertEqual(transaction.target_account, expected_transaction.target_account)
            self.assertEqual(transaction.source_account, expected_transaction.source_account)
