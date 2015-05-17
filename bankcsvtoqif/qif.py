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


class Qif(object):
    """ Interface to .qif-file. """

    def __init__(self, account):
        self.account = account
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def save(self, filename):
        lines = [
            '!Account',
            'N' + self.account,
            '^'
        ]
        for t in self.transactions:
            lines += t.get_lines()

        fp = open(filename, 'w')
        fp.write('\n'.join(lines))
        fp.close()


class Transaction(object):
    """ A qif-Transaction. """

    def __init__(self, date, account, description, amount):
        self.date = date
        self.account = account
        self.description = description
        self.amount = amount

    def get_lines(self):
        return [
            '!Type:Cash',
            'D' + self.date.strftime('%m/%d/%y'),
            'S' + self.account,
            'P' + self.description,
            '$' + '%.2f' % self.amount,
            '^'
        ]
