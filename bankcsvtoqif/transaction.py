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


class Transaction(object):
    """ Represents a transaction obtained from csv-file. """

    def __init__(self, date, description, debit, credit, account):
        self.date = date
        self.description = description
        self.debit = debit
        self.credit = credit
        self.account = account

    def __str__(self):
        return '<Transaction %s, %s, %s, %s, %s>' % (self.date, self.description, self.debit, self.credit, self.account)

    @property
    def amount(self):
        return self.credit - self.debit


class TransactionFactory(object):

    def __init__(self, account_config):
        self.account_config = account_config

    def create_from_line(self, line):
        pass
