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
from bankcsvtoqif.transaction import TransactionFactory

from bankcsvtoqif.banks.vrbank import VRBank


class TestVRBank(unittest.TestCase):
    def setUp(self):
        self.d = VRBank()

    def test_can_instanciate(self):
        pass

    def test_extract_correct_fields(self):
        transaction = (TransactionFactory(self.d)).create_from_line(self.get_fixture_line())

        self.assertIsNotNone(transaction.date)
        self.assertEqual('2015-05-22T00:00:00', transaction.date.isoformat())

        self.assertGreater(transaction.debit, 0)
        self.assertGreater(transaction.debit, 8.2)
        self.assertLess(transaction.debit, 9)
        self.assertEqual(transaction.credit, 0)

        self.assertTrue('AMAZON' in transaction.description)
        self.assertTrue('32132131321' in transaction.description)
        self.assertTrue('-8,21' not in transaction.description)

    def get_fixture_line(self):
        return [
            '1234456789', '22.05.2015', '22.05.2015', 'AMAZON SERVICES EUROPE S.A.R.L.', 'SEPA-Basislastschrift',
            '101-1234567-8910111 Amazon', 'Services Europe SARL 112233', '32132131321', '556465464564', '', '', '',
            '', '', '', '', '', '', '', '-8,21', '138,69', 'EUR'
        ]
