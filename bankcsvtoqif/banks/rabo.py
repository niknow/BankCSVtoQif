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


from bankcsvtoqif.banks import BankAccountConfig
from datetime import datetime


class RaboBank(BankAccountConfig):
    """ Rabo bank current account """

    def __init__(self):
        BankAccountConfig.__init__(self)

        self.encoding = 'windows-1252'
        self.delimiter = ','
        self.quotechar = '"'
        self.dropped_lines = 1
        self.source_account_prefix = 'Assets:Current Assets'
        self.default_target_account = 'Imbalance-EUR'

    def get_date(self, line, all_lines):

        """ line[4] "Datum" is processing date for consumers,
        but the booking date for professional customers.
        Using line[5] "Rentedatum" for now. """

        s = line[5]
        return datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]))

    def get_description(self, line, all_lines):
        description = (line[13],line[9],line[8],line[19],line[24],line[23])
        return ' '.join(description)

    def get_debit(self, line, all_lines):
        amount = self.get_amount(line[6])
        return -amount if amount <= 0 else 0

    def get_credit(self, line, all_lines):
        amount = self.get_amount(line[6])
        return amount if amount >= 0 else 0

    def get_source_account(self, line, all_lines):
        source_account = (self.source_account_prefix, line[0])
        return ':'.join(source_account)
