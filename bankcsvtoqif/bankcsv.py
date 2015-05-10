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


import collections
from itertools import islice
import csv
import qif
from smartlabeler import SmartLabeler


def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


class Transaction(object):
    def __init__(self, date, description, debit, credit, account='Imbalance-EUR'):
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


class BankAccountParserFunctions(object):
    """ Abstract class. For each bank account to be parsed, create a subclass and implement a method
        that gets as an input a line of csv of this bank account and returns as an output the desired
        quantity, i.e. date, description, debit, credit.
    """

    @staticmethod
    def normalize_amount(amount):
        amount = amount.strip('-')
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if not amount:
            return 0
        return float(amount)

    @staticmethod
    def line_to_date(line):
        pass

    @staticmethod
    def line_to_description(line):
        pass

    @staticmethod
    def line_to_debit(line):
        pass

    @staticmethod
    def line_to_credit(line):
        pass


class BankAccountConfig(object):
    def __init__(self):
        self.name = ''
        self.delimiter = ';'
        self.quotechar = '"'
        self.dropped_lines = 5
        self.source_account = 'Assets:Current Assets:Checking Account'
        self.parser_functions = BankAccountParserFunctions
        self.replacements = None


class DataManager(object):
    def __init__(self, csv_filename, qif_filename, account_config):
        self.csv_filename = csv_filename
        self.qif_filename = qif_filename
        self.account_config = account_config
        self.transactions = []

    def read_csv(self):
        f = open(self.csv_filename, 'rb')
        csv.register_dialect(self.account_config.name,
                             delimiter=self.account_config.delimiter,
                             quotechar=self.account_config.quotechar)
        c = csv.reader(f, self.account_config.name)
        consume(c, self.account_config.dropped_lines)  # ignore first lines
        for line in c:
            try:
                par_fun = self.account_config.parser_functions
                transaction = Transaction(par_fun.line_to_date(line),
                                          par_fun.line_to_description(line),
                                          par_fun.line_to_debit(line),
                                          par_fun.line_to_credit(line))
                self.transactions.append(transaction)
            except IndexError:
                print 'skipping: %s' % line
                continue
        f.close()

    def relabel_transactions(self):
        smart_labeler = SmartLabeler()
        smart_labeler.replacements = self.account_config.replacements
        for index, transaction in enumerate(self.transactions):
            self.transactions[index] = smart_labeler.rewrite_description_and_add_account(transaction)

    def write_qif(self):
        q = qif.Qif(self.account_config.source_account)
        for transaction in self.transactions:
            q.add_transaction(
                qif.Transaction(transaction.date, transaction.account, transaction.description, transaction.amount))
        q.save(self.qif_filename)

    def csv_to_qif(self):
        self.read_csv()
        self.relabel_transactions()
        self.write_qif()
