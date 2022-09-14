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

from datetime import datetime

from bankcsvtoqif.banks.comdirect_visa import ComdirectVisa
from bankcsvtoqif.tests.banks import TestBankAccountConfig
from bankcsvtoqif.transaction import Transaction


class TestComdirectVisa(TestBankAccountConfig):
    def testParse(self):
        account_config = ComdirectVisa()
        self.assert_csv_parsed_as(
            "comdirect_visa.csv",
            account_config,
            [
                Transaction(
                    date=datetime(2019, 4, 17),
                    description='some debit',
                    debit=83.00,
                    credit=0,
                    source_account=account_config.default_source_account,
                    target_account=account_config.default_target_account,
                ),
                Transaction(
                    date=datetime(2018, 11, 18),
                    description='some credit',
                    debit=0,
                    credit=123.45,
                    source_account=account_config.default_source_account,
                    target_account=account_config.default_target_account,
                ),
            ]
        )
