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


class QifFile(object):
    """ Interface to .qif-file. """

    def __init__(self, transactions):
        self.transactions = transactions

    def get_raw_data(self):
        lines=[]
        for source_account in self._get_unique_source_accounts():
            lines += self._get_qif_source_account_line(source_account)
            transactions = [t for t in self.transactions if t.source_account==source_account]
            for t in transactions:
                lines += t.to_qif_line()
        return lines

    def _get_unique_source_accounts(self):
        return set([t.source_account for t in self.transactions])

    def _get_qif_source_account_line(self, source_account):
        return [
            '!Account',
            'N' + source_account,
            '^'
        ]