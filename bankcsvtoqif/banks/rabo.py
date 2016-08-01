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

        self.delimiter = ','
        self.quotechar = '"'
        self.dropped_lines = 0
        self.default_source_account = 'Assets:Current Assets:Checking Account'
        self.default_target_account = 'Imbalance-EUR'

    def get_date(self, line):
        s = line[2]
        return datetime(int(s[0:4]), int(s[4:6]), int(s[6:8]))

    def get_description(self, line):
        description = line[10:12]
        return ' '.join(description)

    def get_debit(self, line):
        val = float(line[4])
        return val if line[3] == "D" else 0

    def get_credit(self, line):
        val = float(line[4])
        return val if line[3] == "C" else 0

    def get_source_account(self, line):
        return line[0]
