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


from monthdelta import MonthDelta


class Replacement(object):
    """ A class to automatically handle replacements in transactions. If 'pattern' is matched in the
        original description of a transaction, the description is replaced by 'new_description' and the
        target account 'account' is automatically added. The 'append_date'-flag works as follows:
        append_date = 0: nothing is appended to 'new_description'
        append_date = 1: appends year-month to 'new_description' like 2015-05
        append_date = 2: appends year-next_month to 'new_description' like 2015-06
    """

    def __init__(self, pattern=None, new_description=None, account=None, append_date=0):
        self.pattern = pattern
        self.new_description = new_description
        self.account = account
        self.append_date = append_date

    def matches(self, search_str):
        return self.pattern in search_str

    def should_append_date(self):
        return self.append_date in [1, 2]

    def should_append_next_month_date(self):
        return self.append_date == 2

    def get_description(self, date):
        if not self.should_append_date():
            return self.new_description

        if self.should_append_next_month_date():
            date += MonthDelta(1)
        return self.new_description + ' ' + date.strftime('%Y-%m')


class SmartLabeler(object):
    """ Relabels descriptions of transactions using Replacements.  """

    def __init__(self):
        self.replacements = []

    def rewrite_description_and_add_account(self, transaction):
        for rep in self.replacements:
            if rep.matches(transaction.description):
                transaction.description = rep.get_description(transaction.date)
                transaction.account = rep.account
        return transaction
