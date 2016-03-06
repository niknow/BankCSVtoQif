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

from bankcsvtoqif.banks import BankAccountConfig
from datetime import datetime


class SpardaBank(BankAccountConfig):
    """ Sparda-Bank Girokonto """

    def __init__(self):
        BankAccountConfig.__init__(self)

        self.delimiter = ';'
        self.quotechar = '"'
        self.dropped_lines = 0
        self.default_source_account = 'Assets:Current Assets:Checking Account'
        self.default_target_account = 'Imbalance-EUR'

    def get_date(self, line):
        s = line[0].split('.')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        description = line[2]
        return ' '.join(description.split())

    def get_debit(self, line):
        val = self.get_amount(line[3])
        return -val if val < 0 else 0

    def get_credit(self, line):
        val = self.get_amount(line[3])
        return val if val >= 0 else 0

    def get_target_account(self, line):
        if len(line) == 6:
           s = line[5]
        else:
           s = self.default_target_account;
        return s

