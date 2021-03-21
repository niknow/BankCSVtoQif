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

from bankcsvtoqif.banks.swedbank import Swedbank
from bankcsvtoqif.tests.banks import TestBankAccountConfig
from bankcsvtoqif.transaction import Transaction


class TestSwedbank(TestBankAccountConfig):
    def testParse(self):
        account_config = Swedbank()
        self.assert_csv_parsed_as(
            "swedbank.csv",
            account_config,
            [
                Transaction(
                    date=datetime(2018, 8, 31),
                    description="A transaction",
                    debit=395.00,
                    credit=0,
                    source_account=account_config.default_source_account,
                    target_account=account_config.default_target_account,
                ),
                Transaction(
                    date=datetime(2018, 8, 31),
                    description="This is a credit",
                    debit=0,
                    credit=395.00,
                    source_account=account_config.default_source_account,
                    target_account=account_config.default_target_account,
                ),
                Transaction(
                    date=datetime(2018, 8, 31),
                    description="This is a debit",
                    debit=2135.00,
                    credit=0,
                    source_account=account_config.default_source_account,
                    target_account=account_config.default_target_account,
                ),
            ]
        )
